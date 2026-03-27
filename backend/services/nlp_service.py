import os
import requests
from dotenv import load_dotenv

load_dotenv()

# Production API Configuration per Senior Engineer
HF_TOKEN = os.getenv("HF_TOKEN")
# Stable OpenAI-Compatible Chat Gateway
CHAT_URL = "https://router.huggingface.co/v1/chat/completions"
MODEL_ID = "google/flan-t5-base"

class NLPService:
    def __init__(self):
        """
        Refactored NLP Service for Production.
        Uses Hugging Face's stable OpenAI-compatible API for zero memory footprint.
        """
        self.api_url = CHAT_URL
        self.headers = {
            "Authorization": f"Bearer {HF_TOKEN}",
            "Content-Type": "application/json"
        }

    def _query_hf_api(self, prompt_text: str) -> str:
        """Helper to query the HF OpenAI-Compatible Chat API."""
        payload = {
            "model": MODEL_ID,
            "messages": [{"role": "user", "content": prompt_text}],
            "max_tokens": 1024
        }
        
        try:
            # Strictly following the requested v1 completions format
            response = requests.post(self.api_url, headers=self.headers, json=payload)
            
            if response.status_code == 200:
                result = response.json()
                # OpenAI format: choices[0].message.content
                return result.get("choices", [{}])[0].get("message", {}).get("content", "").strip()
            return f"Error: Chat API returned {response.status_code} - {response.text}"
        except Exception as e:
            return f"AI API Connection Error: {str(e)}"

    def generate_notes(self, transcript_text: str):
        if not transcript_text: return "No transcript provided."
        prompt = f"Summarize this lecture transcript into study notes: {transcript_text[:5000]}"
        return self._query_hf_api(prompt)

    def generate_extra_glossary(self, text: str, explain_like_five: bool = False) -> str:
        if explain_like_five:
             prompt = f"Explain this academic content simply as if to a child: {text[:5000]}"
        else:
             prompt = f"Extract key technical terms and their definitions from: {text[:5000]}"
        return self._query_hf_api(prompt)

    def quick_chat(self, user_query: str) -> str:
        prompt = f"Answer this student question briefly: {user_query}"
        return self._query_hf_api(prompt)
