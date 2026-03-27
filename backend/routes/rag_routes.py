from flask import Blueprint, request, jsonify
from services.rag_service import RAGService

rag_bp = Blueprint('rag', __name__)
rag_service = RAGService()

@rag_bp.route('/index', methods=['POST'])
def index_transcript():
    """Takes a raw transcript and builds a local FAISS/Chroma Vector Store."""
    print("RAG ROUTE: /index accessed.")
    data = request.get_json()
    if not data or 'text' not in data:
         print("RAG ROUTE ERROR: Missing text parameter.")
         return jsonify({"error": "Missing 'text' parameter for indexing"}), 400
         
    try:
        print(f"RAG ROUTE: Indexing document of length {len(data['text'])}")
        session_id = rag_service.index_document(data['text'])
        print(f"RAG ROUTE: Indexing successful. Session ID: {session_id}")
        return jsonify({"message": "Transcript indexed successfully.", "session_id": session_id}), 200
    except Exception as e:
        print(f"RAG ROUTE ERROR: {str(e)}")
        return jsonify({"error": str(e)}), 500


@rag_bp.route('/chat', methods=['POST'])
def chat_with_lecture():
    """Queries the indexed lecture and responds using RAG pipeline."""
    print("RAG ROUTE: /chat accessed.")
    data = request.get_json()
    if not data or 'query' not in data or 'session_id' not in data:
        print("RAG ROUTE ERROR: Missing query or session_id.")
        return jsonify({"error": "Missing 'query' or 'session_id'"}), 400
        
    try:
        print(f"RAG ROUTE: Querying session {data['session_id']} for query: {data['query']}")
        response = rag_service.query_document(data['session_id'], data['query'])
        print("RAG ROUTE: Query complete.")
        return jsonify({"answer": response}), 200
    except Exception as e:
        print(f"RAG ROUTE ERROR: {str(e)}")
        return jsonify({"error": str(e)}), 500
