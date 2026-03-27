import os
# Fix for protobuf version conflicts
os.environ["PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION"] = "python"

from flask import Flask, jsonify
from flask_cors import CORS

from routes.audio_routes import audio_bp
from routes.nlp_routes import nlp_bp
from routes.rag_routes import rag_bp

def create_app():
    """
    Application factory for the Flask backend.
    """
    app = Flask(__name__)
    
    # Simple CORS configuration to allow all origins
    CORS(app)

    # Register API Blueprints
    app.register_blueprint(audio_bp, url_prefix='/api/audio')
    app.register_blueprint(nlp_bp, url_prefix='/api/nlp')
    app.register_blueprint(rag_bp, url_prefix='/api/rag')

    @app.route('/api/health', methods=['GET'])
    def health_check():
        print(">>> HEALTH CHECK HIT <<<")
        return jsonify({"status": "ok", "message": "Lecture AI Flask Backend is running on port 5000."}), 200

    @app.route('/api/test', methods=['GET'])
    def test_connection():
        print(">>> TEST ENDPOINT HIT <<<")
        return jsonify({"status": "success", "message": "Backend is reachable on port 5000!"}), 200

    @app.errorhandler(Exception)
    def handle_exception(e):
        """Global exception handler"""
        print(f"!!! SERVER ERROR !!! : {str(e)}")
        return jsonify({"error": str(e)}), 500

    return app

if __name__ == "__main__":
    app = create_app()
    # PORT 5000 as per user request
    print("--------------------------------------------------")
    print("Starting Flask Backend on http://localhost:5000")
    print("--------------------------------------------------")
    app.run(host="0.0.0.0", port=5000, debug=True)
