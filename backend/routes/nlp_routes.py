from flask import Blueprint, request, jsonify
from services.nlp_service import NLPService
from services.assessment_service import AssessmentService

nlp_bp = Blueprint('nlp', __name__)
nlp_service = NLPService()
assessment_service = AssessmentService()

@nlp_bp.route('/notes', methods=['POST'])
def generate_notes():
    """Generates strictly structured academic notes."""
    print("NLP ROUTE: /notes accessed.")
    data = request.get_json()
    if not data or 'text' not in data:
        print("NLP ROUTE ERROR: Missing input text.")
        return jsonify({"error": "Missing input text"}), 400
        
    notes = nlp_service.generate_notes(data['text'])
    return jsonify({"notes": notes}), 200

@nlp_bp.route('/extra', methods=['POST'])
def generate_extra_glossary():
    """Extracts complex terms for a deep-dive glossary."""
    print("NLP ROUTE: /extra accessed.")
    data = request.get_json()
    if not data or 'text' not in data:
        return jsonify({"error": "Missing input text"}), 400
        
    eli5_mode = data.get('eli5', False)
    extra_content = nlp_service.generate_extra_glossary(data['text'], explain_like_five=eli5_mode)
    
    return jsonify({"extra_glossary": extra_content}), 200

@nlp_bp.route('/assess', methods=['POST'])
def generate_assessments():
    """Autonomously builds QA flashcards/quizzes from notes via AssessmentService."""
    print("NLP ROUTE: /assess accessed.")
    data = request.get_json()
    if not data or 'notes' not in data:
         return jsonify({"error": "Missing structured notes text"}), 400
         
    assessments = assessment_service.generate_quiz_cards(data['notes'])
    return jsonify({"assessments": assessments}), 200

@nlp_bp.route('/chat', methods=['POST'])
def general_chat():
    """New direct chat endpoint for Vynote AI Workspace."""
    print("NLP ROUTE: /chat accessed.")
    data = request.get_json()
    if not data or 'query' not in data:
         return jsonify({"error": "Missing query"}), 400
         
    answer = nlp_service.quick_chat(data['query'])
    return jsonify({"answer": answer}), 200
