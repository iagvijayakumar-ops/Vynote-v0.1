import os
import requests
import uuid
from dotenv import load_dotenv

load_dotenv()

class RAGService:
    def __init__(self):
        """
        Refactored RAG Service for Production (Zero-Memory footprint).
        Uses Hugging Face Inference API for embeddings and dot-product in pure Python.
        Replaces ChromaDB, Torch, and LangChain for Render free tier stability.
        """
        self.api_token = os.getenv("HF_TOKEN")
        # Lightweight and accurate embedding model for API inference
        self.model_id = "sentence-transformers/all-MiniLM-L6-v2"
        self.api_url = f"https://api-inference.huggingface.co/models/{self.model_id}"
        self.headers = {"Authorization": f"Bearer {self.api_token}"} if self.api_token else {}
        
        # Session storage: session_id -> { "chunks": [str], "embeddings": [[float]] }
        self.sessions = {}

    def _get_embedding(self, text: str):
        """Helper to get text embeddings from HF API."""
        response = requests.post(self.api_url, headers=self.headers, json={"inputs": text})
        if response.status_code == 200:
            return response.json()
        return None

    def index_document(self, transcript_text: str) -> str:
        """Chunks the transcript and pre-computes embeddings via API."""
        if not transcript_text: return None
        
        # 1. Simple Chunking (approx 500 chars)
        chunks = [transcript_text[i:i+500] for i in range(0, len(transcript_text), 400)]
        print(f"RAG SERVICE: Chinking transcript into {len(chunks)} segments...")

        # 2. Get embeddings for all chunks via HF
        # Note: In production we'd batch this, but for simplicity we map it
        session_data = {"chunks": chunks, "embeddings": []}
        
        # Batching for HF API stability
        response = requests.post(self.api_url, headers=self.headers, json={"inputs": chunks})
        if response.status_code == 200:
            session_data["embeddings"] = response.json()
            session_id = str(uuid.uuid4())
            self.sessions[session_id] = session_data
            return session_id
        
        print(f"RAG SERVICE ERROR: Chunk indexing failed. {response.text}")
        return None

    def query_document(self, session_id: str, query: str) -> str:
        """
        Retrieves context using cosine-similarity (pure Python) and 
        returns the query + context for the NLP service to handle.
        """
        if session_id not in self.sessions: return "Session expired or missing."
        
        session = self.sessions[session_id]
        query_embedding = self._get_embedding(query)
        
        if not query_embedding: return "Search engine currently offline."
        
        # 3. Simple cosine similarity search across cached embeddings
        scores = []
        for idx, chunk_emb in enumerate(session["embeddings"]):
            # Dot product (both normalized by HF)
            score = sum(a * b for a, b in zip(query_embedding, chunk_emb))
            scores.append((score, idx))
            
        scores.sort(key=lambda x: x[0], reverse=True)
        top_chunks = [session["chunks"][idx] for _, idx in scores[:2]] # Top 2 context chunks
        context = " ".join(top_chunks)
        
        # 4. Final Answer Generation via API (Mistral)
        # We reuse the NLP methodology here for zero local CPU load
        nlp_token = os.getenv("HF_TOKEN")
        nlp_url = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.3"
        nlp_headers = {"Authorization": f"Bearer {nlp_token}"}
        
        prompt = f"Using this context: '{context}', answer the user question briefly: '{query}'"
        payload = {"inputs": f"<s>[INST] {prompt} [/INST]", "parameters": {"max_new_tokens": 512}}
        
        try:
            res = requests.post(nlp_url, headers=nlp_headers, json=payload)
            if res.status_code == 200:
                answer = res.json()
                if isinstance(answer, list): return answer[0].get("generated_text", "").strip()
                return answer.get("generated_text", "").strip()
            return f"Search result found context but failed to generate answer: {context[:100]}..."
        except Exception as e:
            return f"RAG Search failed: {str(e)}"
