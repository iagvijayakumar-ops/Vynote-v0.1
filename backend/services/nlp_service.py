import os
from langchain_ollama import OllamaLLM
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv

load_dotenv()

class NLPService:
    def __init__(self):
        """
        Initializes the NLP Service with optimized lightweight models for CPU.
        Primary: phi3 (3.8B) - approx 3-4x faster than llama3 on CPU.
        """
        print("NLP Service: Initializing with Phi-3 (Fast & Free)...")
        try:
             # phi3 is chosen for its extreme speed and efficiency on consumer hardware
             self.llm = OllamaLLM(model="phi3")
        except Exception as e:
             print(f"NLP Service Warning: Ollama not reachable / model not found. {e}")
             self.llm = None

    def generate_notes(self, transcript_text: str):
        """
        Optimized note generation using high-quality but concise prompting.
        Truncates long inputs to ensure stable CPU inference.
        """
        if not transcript_text or len(transcript_text.strip()) < 50:
            return "Transcript too short to generate notes."

        if self.llm is None:
             return "Ollama (phi3) required. Run 'ollama run phi3'."

        # PROMPT OPTIMIZATION: Shortened instructions for faster generation
        truncated_text = transcript_text[:8000] 

        template = """
        System: You are an expert academic scribe. Rewrite the lecture text into structured notes.
        Format:
        📘 Title: [Short & Academic]
        📌 Key Points:
        1. [Topic]: [Clear explanation]
        2. ...
        
        Transcript: "{text}"
        
        Final Notes:
        """
        
        prompt = PromptTemplate(input_variables=["text"], template=template)
        formatted = prompt.format(text=truncated_text)
        
        try:
             return self.llm.invoke(formatted)
        except Exception as e:
             return f"Generation failed: {str(e)}"

    def generate_extra_glossary(self, text: str, explain_like_five: bool = False) -> str:
        """
        Fast glossary extraction with minimal instructions.
        """
        if self.llm is None: return "Ollama required."
        
        truncated_text = text[:4000] 
              
        if explain_like_five:
             template = 'Explain the core concept of this text to a 5-year old: "{text}"'
        else:
             template = 'Extract 5 key terms and definitions from this text: "{text}"'
             
        prompt = PromptTemplate(input_variables=["text"], template=template)
        formatted = prompt.format(text=truncated_text)
        
        try:
             return self.llm.invoke(formatted)
        except Exception as e:
             return f"Failed: {str(e)}"

    def quick_chat(self, user_query: str) -> str:
        """
        Direct chat with LLM (phi3) for general queries or academic discussion.
        Used for the new full-page chat feature in 'Vynote'.
        """
        if self.llm is None:
             return "AI Backend Offline. Ensure Ollama 'phi3' is running."
             
        # Optimized system prompt for Vynote assistant
        template = """
        System: You are 'Vynote AI', a premium academic assistant. 
        Be professional, concise, and smart. Assist the user with their question.
        
        User: {query}
        Vynote AI: 
        """
        
        prompt = PromptTemplate(input_variables=["query"], template=template)
        formatted = prompt.format(query=user_query)
        
        try:
             return self.llm.invoke(formatted)
        except Exception as e:
             return f"Chat error: {str(e)}"
