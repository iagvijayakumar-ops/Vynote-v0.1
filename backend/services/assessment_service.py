import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

# Production API Configuration per Senior Engineer
HF_TOKEN = os.getenv("HF_TOKEN")
HEADERS = {"Authorization": f"Bearer {HF_TOKEN}"} if HF_TOKEN else {}
# Upgraded Inference Router Endpoint (Flan-T5-Large)
API_URL = "https://router.huggingface.co/hf-inference/models/google/flan-t5-large"

class AssessmentService:
    def __init__(self):
        """
        Refactored Assessment Service for Production.
        Uses external Hugging Face Inference API for study tool generation.
        """
        self.api_url = API_URL
        self.headers = HEADERS

    def generate_quiz_cards(self, structured_notes: str) -> dict:
        """Generates Quiz and Flashcards via external API."""
        if not structured_notes: return {"error": "Empty notes."}
        
        # Flan-T5-Large is highly instruction-tuned and stable for JSON tasks
        prompt = f"Convert these notes into a JSON object with 3 flashcards and 2 MCQ quizzes: {structured_notes[:2000]}"
        
        payload = {"inputs": prompt, "parameters": {"max_new_tokens": 800}}
        
        try:
            # CORRECT FORMAT FOR FLAN-T5: json={"inputs": prompt} on the hf-inference route
            res = requests.post(self.api_url, headers=self.headers, json=payload)
            if res.status_code == 200:
                text = res.json()
                if isinstance(text, list): text = text[0].get("generated_text", "{}")
                else: text = text.get("generated_text", "{}")
                
                # Cleanup for JSON extraction
                try:
                    clean_text = text.replace("```json", "").replace("```", "").strip()
                    return json.loads(clean_text)
                except:
                     # Fallback if BART fails to return perfect JSON
                     return {
                         "flashcards": [{"front": "Summary", "back": text}],
                         "quizzes": []
                     }
            return {"error": f"API Error {res.status_code}"}
        except Exception as e:
            return {"error": f"Assessment generation failed: {str(e)}"}
