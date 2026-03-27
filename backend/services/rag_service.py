import os
import uuid
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_ollama import OllamaLLM
from langchain.chains import RetrievalQA
import tempfile

class RAGService:
    def __init__(self):
        """Initializes the Retrieval-Augmented Generation pipeline with fast components."""
        print("RAG Service: Initializing Embedding Model (all-MiniLM-L6-v2) - Small & Fast")
        # Lightweight embedding model. Fits easily in memory.
        self.embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        
        # Session cache
        self.vector_stores = {}
        
        print("RAG Service: Loading Phi-3 for conversational recall...")
        try:
             # Phi-3 is extremely efficient for RAG tasks with lower latency
             self.llm = OllamaLLM(model="phi3") 
        except Exception as e:
             print(f"RAG Service Warning: Ollama/Phi3 not found. {e}")
             self.llm = None

    def index_document(self, transcript_text: str) -> str:
        """
        Chunks transcript. Reduced chunk size for faster retrieval and smaller prompts.
        """
        if not transcript_text:
            raise ValueError("Transcript text empty.")

        fd, path = tempfile.mkstemp(suffix=".txt")
        with os.fdopen(fd, 'w', encoding='utf-8') as f:
            f.write(transcript_text)

        loader = TextLoader(path, encoding='utf-8')
        documents = loader.load()

        # SPEED OPTIMIZATION: Small chunking (500 characters) leads to faster prompt resolution
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
        docs = text_splitter.split_documents(documents)

        session_id = str(uuid.uuid4())
        
        # Entirely in-memory for session speed
        vectorstore = Chroma.from_documents(documents=docs, embedding=self.embeddings)
        self.vector_stores[session_id] = vectorstore

        os.remove(path)
        return session_id

    def query_document(self, session_id: str, query: str) -> str:
        """
        Queries session. Optimized retrieval parameters (k=2) for smaller contexts.
        """
        if session_id not in self.vector_stores:
             raise ValueError(f"Session expired: {session_id}")
             
        vectorstore = self.vector_stores[session_id]
        
        if self.llm is None:
             docs = vectorstore.similarity_search(query, k=1)
             context = "\n".join([d.page_content for d in docs])
             return f"Local LLM Offline. Suggestion: {context}"

        # OPTIMIZATION: Lower k value (2 instead of 3) = Smaller prompts sent to LLM
        qa_chain = RetrievalQA.from_chain_type(
            self.llm,
            retriever=vectorstore.as_retriever(search_kwargs={"k": 2}),
            return_source_documents=False
        )
        
        # DIRECT PROMPT: Shorter query instruction
        fast_query = f"Using this context, answer briefly: {query}"
        
        try:
             result = qa_chain.invoke({"query": fast_query})
             return result.get('result', "No answer found.")
        except Exception as e:
             return f"RAG Query Failed: {str(e)}"
