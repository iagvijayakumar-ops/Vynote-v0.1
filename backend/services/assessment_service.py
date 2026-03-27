import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

# Production API Configuration
HF_TOKEN = os.getenv("HF_TOKEN")
HEADERS = {"Authorization": f"Bearer {HF_TOKEN}"} if HF_TOKEN else {}
# Corrected Router Endpoint
API_URL = "https://router.huggingface.co/hf-inference/models/mistralai/Mistral-7B-Instruct-v0.3"

class AssessmentService:
    def __init__(self):
        """
        Refactored Assessment Service for Production.
        Uses external Hugging Face Inference API for JSON-based quiz generation.
        """
        self.api_url = API_URL
        self.headers = HEADERS

    def generate_quiz_cards(self, structured_notes: str) -> dict:
        """Generates Quiz and Flashcards via external API."""
        if not structured_notes: return {"error": "Empty notes."}
        
        prompt = f"""
        Act as an expert academic educator. Based on these lecture notes, 
        generate:
        1. 3 Flashcards (front/back)
        2. 2 Multiple Choice Questions (with 4 options and 1 correct answer)
        
        Return the result ONLY as a raw JSON object with this exact schema:
        {{
            "flashcards": [ {{"front": "...", "back": "..."}} ],
            "quizzes": [ {{"question": "...", "options": ["...", "...", "...", "..."], "answer": "..."}} ]
        }}
        
        NOTES:
        {structured_notes[:5000]}
        
        JSON:
        """
        
        payload = {
            "inputs": f"<s>[INST] {prompt} [/INST]",
            "parameters": {"max_new_tokens": 800, "temperature": 0.1, "return_full_text": False}
        }
        
        try:
            res = requests.post(self.api_url, headers=self.headers, json=payload)
            if res.status_code == 200:
                text = res.json()
                if isinstance(text, list): text = text[0].get("generated_text", "{}")
                else: text = text.get("generated_text", "{}")
                
                clean_text = text.replace("```json", "").replace("```", "").strip()
                return json.loads(clean_text)
            return {"error": f"API Error {res.status_code}"}
        except Exception as e:
            return {"error": f"Assessment generation failed: {str(e)}"}
