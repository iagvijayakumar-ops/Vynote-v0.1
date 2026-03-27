import os
import requests
from dotenv import load_dotenv

load_dotenv()

class NLPService:
    def __init__(self):
        """
        Refactored NLP Service for Production.
        Uses Hugging Face Inference API (Mistral-7B or Phi-3) 
        instead of local Ollama for zero memory footprint on Render.
        """
        self.api_token = os.getenv("HF_TOKEN")
        # Mistral-7B-Instruct is a high-quality production-ready instruction model
        self.model_id = "mistralai/Mistral-7B-Instruct-v0.3"
        self.api_url = f"https://router.huggingface.co/hf-inference/models/{self.model_id}"
        self.headers = {"Authorization": f"Bearer {self.api_token}"} if self.api_token else {}

        if not self.api_token:
            print("WARNING: HF_TOKEN not set in NLPService. AI generation will fail.")

    def _query_hf_api(self, prompt_text: str) -> str:
        """Helper to query the HF Inference API."""
        payload = {
            "inputs": f"<s>[INST] {prompt_text} [/INST]",
            "parameters": {"max_new_tokens": 1024, "top_k": 30, "return_full_text": False}
        }
        
        try:
            response = requests.post(self.api_url, headers=self.headers, json=payload)
            if response.status_code == 200:
                result = response.json()
                # Handle both list responses and dictionary responses from HF
                if isinstance(result, list) and len(result) > 0:
                    return result[0].get("generated_text", "").strip()
                return result.get("generated_text", "").strip()
            return f"Error: API returned {response.status_code} - {response.text}"
        except Exception as e:
            return f"AI API Connection Error: {str(e)}"

    def generate_notes(self, transcript_text: str):
        """Standard note generation via external API."""
        if not transcript_text: return "No transcript provided."
        
        prompt = f"""
        System: Act as an elite academic scribe. Transform this lecture transcript into structured notes.
        Instructions: 
        1. Create a Descriptive Title.
        2. Identify 5-7 Key Concepts with clear explanations.
        3. Use Markdown.
        
        Transcript: "{transcript_text[:10000]}"
        
        Final Notes:
        """
        return self._query_hf_api(prompt)

    def generate_extra_glossary(self, text: str, explain_like_five: bool = False) -> str:
        """Glossary extraction via external API."""
        if explain_like_five:
             prompt = f"Explain the core message of this academic text to 5-year-old: '{text[:8000]}'"
        else:
             prompt = f"Extract 5 key technical terms and their one-sentence definitions from this text: '{text[:8000]}'"
             
        return self._query_hf_api(prompt)

    def quick_chat(self, user_query: str) -> str:
        """Discussion assistant via external API."""
        prompt = f"System: You are 'Vynote AI', a helpful student assistant. Be concise.\nUser: {user_query}\nVynote AI:"
        return self._query_hf_api(prompt)
