import os
import requests
from dotenv import load_dotenv

load_dotenv()

# Production API Configuration per Senior Engineer
HF_TOKEN = os.getenv("HF_TOKEN")
HEADERS = {"Authorization": f"Bearer {HF_TOKEN}"} if HF_TOKEN else {}
# Corrected Router Endpoint per Senior Engineer instructions
API_URL = "https://router.huggingface.co/hf-inference/models/mistralai/Mistral-7B-Instruct-v0.3"

class NLPService:
    def __init__(self):
        """
        Refactored NLP Service for Production.
        Uses Hugging Face Inference API for zero memory footprint on Render.
        """
        self.api_url = API_URL
        self.headers = HEADERS

    def _query_hf_api(self, prompt_text: str) -> str:
        """
        Helper to query the HF Inference API.
        CORRECT FORMAT FOR TEXT MODELS: JSON with 'inputs' field.
        """
        # Strictly following requested JSON format: {"inputs": prompt}
        payload = {
            "inputs": f"<s>[INST] {prompt_text} [/INST]",
            "parameters": {"max_new_tokens": 1024} # Keep minimal necessary
        }
        
        try:
            # We use json= here, NOT data= per instructions
            response = requests.post(self.api_url, headers=self.headers, json=payload)
            
            if response.status_code == 200:
                result = response.json()
                if isinstance(result, list) and len(result) > 0:
                    return result[0].get("generated_text", "").strip()
                return result.get("generated_text", "").strip()
            return f"Error: API returned {response.status_code} - {response.text}"
        except Exception as e:
            return f"AI API Connection Error: {str(e)}"

    def generate_notes(self, transcript_text: str):
        if not transcript_text: return "No transcript provided."
        prompt = f"System: Act as an academic scribe. Transform this transcript into notes: '{transcript_text[:10000]}'"
        return self._query_hf_api(prompt)

    def generate_extra_glossary(self, text: str, explain_like_five: bool = False) -> str:
        if explain_like_five:
             prompt = f"Explain the core message of this academic text to 5-year-old: '{text[:8000]}'"
        else:
             prompt = f"Extract 5 technical terms and definitions: '{text[:8000]}'"
        return self._query_hf_api(prompt)

    def quick_chat(self, user_query: str) -> str:
        prompt = f"You are 'Vynote AI', a student assistant. User: {user_query}"
        return self._query_hf_api(prompt)
