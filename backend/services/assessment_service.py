import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

# Production API Configuration per Senior Engineer
HF_TOKEN = os.getenv("HF_TOKEN")
# Stable OpenAI-Compatible Chat Gateway
CHAT_URL = "https://router.huggingface.co/v1/chat/completions"
MODEL_ID = "google/flan-t5-base"

class AssessmentService:
    def __init__(self):
        """
        Refactored Assessment Service for Production.
        Uses Hugging Face's OpenAI-compatible Chat API for zero memory footprint.
        """
        self.api_url = CHAT_URL
        self.headers = {
            "Authorization": f"Bearer {HF_TOKEN}",
            "Content-Type": "application/json"
        }

    def generate_quiz_cards(self, structured_notes: str) -> dict:
        """Generates Quiz and Flashcards via external API."""
        if not structured_notes: return {"error": "Empty notes."}
        
        prompt = f"Convert these notes into a JSON object with 3 flashcards and 2 MCQ quizzes: {structured_notes[:2000]}"
        
        payload = {
            "model": MODEL_ID,
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 800
        }
        
        try:
            # We use json= here per instructions
            res = requests.post(self.api_url, headers=self.headers, json=payload)
            
            if res.status_code == 200:
                result = res.json()
                # Parse OpenAI response: choices[0].message.content
                text = result.get("choices", [{}])[0].get("message", {}).get("content", "").strip()
                
                # Cleanup for JSON extraction
                try:
                    clean_text = text.replace("```json", "").replace("```", "").strip()
                    return json.loads(clean_text)
                except:
                     # Fallback if t5-base does not return perfect JSON
                     return {
                         "flashcards": [{"front": "Summary", "back": text}],
                         "quizzes": []
                     }
            return {"error": f"API Error {res.status_code}"}
        except Exception as e:
            return {"error": f"Assessment generation failed: {str(e)}"}
