import os
import requests
from dotenv import load_dotenv

load_dotenv()

# Production API Configuration per Senior Engineer
HF_TOKEN = os.getenv("HF_TOKEN")
HEADERS = {"Authorization": f"Bearer {HF_TOKEN}"} if HF_TOKEN else {}
# Corrected Inference Router Endpoint
API_URL = "https://router.huggingface.co/hf-inference/models/facebook/bart-large-cnn"

class NLPService:
    def __init__(self):
        """
        Refactored NLP Service for Production.
        Uses Hugging Face Inference API for zero memory footprint on Render.
        """
        self.api_url = API_URL
        self.headers = HEADERS

    def _query_hf_api(self, prompt_text: str) -> str:
        """Helper to query the HF Inference API."""
        # Strictly following the requested format: json={"inputs": prompt}
        payload = {"inputs": prompt_text}
        
        try:
            response = requests.post(self.api_url, headers=self.headers, json=payload)
            if response.status_code == 200:
                result = response.json()
                # BART-large-cnn returns a list by default
                if isinstance(result, list) and len(result) > 0:
                    return result[0].get("summary_text", "").strip() or result[0].get("generated_text", "").strip()
                return result.get("generated_text", "").strip()
            return f"Error: API returned {response.status_code} - {response.text}"
        except Exception as e:
            return f"AI API Connection Error: {str(e)}"

    def generate_notes(self, transcript_text: str):
        if not transcript_text: return "No transcript provided."
        prompt = f"Summarize this lecture into notes: {transcript_text[:5000]}"
        return self._query_hf_api(prompt)

    def generate_extra_glossary(self, text: str, explain_like_five: bool = False) -> str:
        if explain_like_five:
             prompt = f"Explain this academic text simply: {text[:5000]}"
        else:
             prompt = f"List technical terms and their definitions from: {text[:5000]}"
        return self._query_hf_api(prompt)

    def quick_chat(self, user_query: str) -> str:
        prompt = f"Answer this question briefly: {user_query}"
        return self._query_hf_api(prompt)
