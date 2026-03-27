import os
import requests
from dotenv import load_dotenv

load_dotenv()

# Production API Configuration per Senior Engineer
HF_TOKEN = os.getenv("HF_TOKEN")
HEADERS = {"Authorization": f"Bearer {HF_TOKEN}"} if HF_TOKEN else {}
# Upgraded Inference Router Endpoint (Zephyr-7B-Beta)
API_URL = "https://router.huggingface.co/hf-inference/models/HuggingFaceH4/zephyr-7b-beta"

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
        # Zephyr-7B-Beta works best with simple instruction prompting
        formatted_prompt = f"<|system|>\nYou are Vynote AI, a helpful student assistant.</s>\n<|user|>\n{prompt_text}</s>\n<|assistant|>\n"
        payload = {"inputs": formatted_prompt, "parameters": {"max_new_tokens": 800, "return_full_text": False}}
        
        try:
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
        prompt = f"Transform this transcript into detailed study notes with a clear title and bullet points: {transcript_text[:5000]}"
        return self._query_hf_api(prompt)

    def generate_extra_glossary(self, text: str, explain_like_five: bool = False) -> str:
        if explain_like_five:
             prompt = f"Explain this academic content as if to a child: {text[:5000]}"
        else:
             prompt = f"Extract key technical terms and their one-sentence definitions from: {text[:5000]}"
        return self._query_hf_api(prompt)

    def quick_chat(self, user_query: str) -> str:
        prompt = f"Answer this student question concisely: {user_query}"
        return self._query_hf_api(prompt)
