import os
import requests
import uuid
from dotenv import load_dotenv

load_dotenv()

# Production API Configuration per Senior Engineer
HF_TOKEN = os.getenv("HF_TOKEN")
HEADERS = {"Authorization": f"Bearer {HF_TOKEN}"} if HF_TOKEN else {}
# Official Inference Endpoints (Stable)
EMBED_URL = "https://api-inference.huggingface.co/models/sentence-transformers/all-MiniLM-L6-v2"
CHAT_URL = "https://api-inference.huggingface.co/models/google/flan-t5-large"

class RAGService:
    def __init__(self):
        """
        Refactored RAG Service for Production (Zero-Memory footprint).
        Uses official Hugging Face Inference API for stability.
        """
        self.headers = HEADERS
        self.sessions = {}

    def _get_embedding(self, text: str):
        """Helper to get text embeddings from HF API."""
        response = requests.post(EMBED_URL, headers=self.headers, json={"inputs": text})
        if response.status_code == 200:
            return response.json()
        return None

    def index_document(self, transcript_text: str) -> str:
        if not transcript_text: return None
        chunks = [transcript_text[i:i+500] for i in range(0, len(transcript_text), 400)]
        print(f"RAG SERVICE: Chinking transcript into {len(chunks)} segments...")
        session_data = {"chunks": chunks, "embeddings": []}
        
        response = requests.post(EMBED_URL, headers=self.headers, json={"inputs": chunks})
        if response.status_code == 200:
            session_data["embeddings"] = response.json()
            session_id = str(uuid.uuid4())
            self.sessions[session_id] = session_data
            return session_id
        
        print(f"RAG SERVICE ERROR: Chunk indexing failed. {response.text}")
        return None

    def query_document(self, session_id: str, query: str) -> str:
        if session_id not in self.sessions: return "Session expired or missing."
        
        session = self.sessions[session_id]
        query_embedding = self._get_embedding(query)
        
        if not query_embedding: return "Search engine currently offline."
        
        scores = []
        for idx, chunk_emb in enumerate(session["embeddings"]):
            score = sum(a * b for a, b in zip(query_embedding, chunk_emb))
            scores.append((score, idx))
            
        scores.sort(key=lambda x: x[0], reverse=True)
        top_chunks = [session["chunks"][idx] for _, idx in scores[:2]]
        context = " ".join(top_chunks)
        
        prompt = f"Answer this question briefly based on the provided context. Context: '{context}' Question: '{query}'"
        payload = {"inputs": prompt}
        
        try:
            # Shifted to official API from router for stability
            res = requests.post(CHAT_URL, headers=self.headers, json=payload)
            if res.status_code == 200:
                answer = res.json()
                if isinstance(answer, list) and len(answer) > 0:
                    return answer[0].get("generated_text", "").strip()
                return answer.get("generated_text", "").strip()
            return f"Search result found context but failed into generate answer: {context[:100]}..."
        except Exception as e:
            return f"RAG Search failed: {str(e)}"
