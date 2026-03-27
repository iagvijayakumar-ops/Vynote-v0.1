import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

# Production API Configuration per Senior Engineer
HF_TOKEN = os.getenv("HF_TOKEN")
HEADERS = {"Authorization": f"Bearer {HF_TOKEN}"} if HF_TOKEN else {}
# Official Inference Endpoint (Stable)
API_URL = "https://api-inference.huggingface.co/models/google/flan-t5-large"

class AssessmentService:
    def __init__(self):
        """
        Refactored Assessment Service for Production.
        Uses official Hugging Face Inference API for zero memory footprint.
        """
        self.api_url = API_URL
        self.headers = HEADERS

    def generate_quiz_cards(self, structured_notes: str) -> dict:
        """Generates Quiz and Flashcards via external API."""
        if not structured_notes: return {"error": "Empty notes."}
        
        prompt = f"Convert these notes into a JSON object with 3 flashcards and 2 MCQ quizzes: {structured_notes[:2000]}"
        
        try:
            # We use json= here per instructions
            res = requests.post(self.api_url, headers=self.headers, json={"inputs": prompt})
            if res.status_code == 200:
                text = res.json()
                if isinstance(text, list): text = text[0].get("generated_text", "{}")
                else: text = text.get("generated_text", "{}")
                
                # Cleanup for JSON extraction
                try:
                    clean_text = text.replace("```json", "").replace("```", "").strip()
                    return json.loads(clean_text)
                except:
                     return {
                         "flashcards": [{"front": "Summary", "back": text}],
                         "quizzes": []
                     }
            return {"error": f"API Error {res.status_code}"}
        except Exception as e:
            return {"error": f"Assessment generation failed: {str(e)}"}
