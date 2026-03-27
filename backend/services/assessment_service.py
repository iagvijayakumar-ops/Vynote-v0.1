import json
from langchain_ollama import OllamaLLM
from langchain_core.prompts import PromptTemplate

class AssessmentService:
    def __init__(self):
        """Initializes the Automated Assessment Generator using Ollama via langchain_ollama."""
        try:
            # Using Llama 3 via Ollama for complex parsing and JSON generation
            # format="json" ensures strict JSON structure output.
            self.llm = OllamaLLM(model="llama3", format="json")
        except Exception as e:
            print(f"Assessment Service Warning: Ollama not reachable. {e}")
            self.llm = None

    def generate_quiz_cards(self, structured_notes: str) -> dict:
         """
         Takes structured notes and autonomously generates Flashcards and MCQs.
         """
         if not structured_notes:
              return {"error": "Empty notes provided"}
              
         if self.llm is None:
              # Mock return if no local LLM is running
              return {
                  "flashcards": [{"front": "What is the title?", "back": "Check the notes."}],
                  "quizzes": [{"question": "Did this work?", "options": ["Yes", "No", "Mock"], "answer": "Mock"}]
              }

         prompt_template = PromptTemplate(
            input_variables=["notes"],
            template="""
            Act as an expert educator. Based ONLY on the following lecture notes, generate:
            1. 3 Q&A Flashcards for core concepts.
            2. 2 Multiple Choice Questions (with 4 options and 1 correct answer).
            
            Return the output STRICTLY as a JSON object with this exact schema and no markdown formatting:
            {{
                "flashcards": [
                    {{"front": "string", "back": "string"}}
                ],
                "quizzes": [
                    {{"question": "string", "options": ["string", "string", "string", "string"], "answer": "string"}}
                ]
            }}

            LECTURE NOTES:
            {notes}
            """
         )
         
         formatted_prompt = prompt_template.format(notes=structured_notes)
         
         try:
             # Force strict JSON output with format="json" in OllamaLLM
             response_text = self.llm.invoke(formatted_prompt)
             
             # Parse and validate returned JSON
             assessment_data = json.loads(response_text)
             return assessment_data
             
         except json.JSONDecodeError as je:
             print(f"Failed to parse LLM JSON: {je}. Raw output: {response_text}")
             return {"error": "LLM failed to output valid JSON framework."}
         except Exception as e:
             return {"error": str(e)}
