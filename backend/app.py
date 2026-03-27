import os
from flask import Flask, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

# Absolute imports from the backend root
from routes.audio_routes import audio_bp
from routes.nlp_routes import nlp_bp
from routes.rag_routes import rag_bp

load_dotenv()

def create_app():
    """
    Application factory for the Vynote Flask backend.
    Refactored for production-level stability (Free tier 512MB RAM).
    """
    app = Flask(__name__)
    
    # 1. CORS: Enable for Netlify frontend in production
    CORS(app)

    # 2. Register Blueprints (Clean modular architecture)
    app.register_blueprint(audio_bp, url_prefix='/api/audio')
    app.register_blueprint(nlp_bp, url_prefix='/api/nlp')
    app.register_blueprint(rag_bp, url_prefix='/api/rag')

    @app.route('/api/health', methods=['GET'])
    def health_check():
        """Health check for Render/Netlify deployments."""
        return jsonify({
            "status": "ok", 
            "message": "Vynote Backend is online.",
            "mode": "Production (API Inference)"
        }), 200

    @app.route('/api/test', methods=['GET'])
    def test_connection():
        """Simple reachability test for the React frontend."""
        return jsonify({
            "status": "success", 
            "message": "Vynote API reachable."
        }), 200

    @app.errorhandler(Exception)
    def handle_exception(e):
        """Production error handling to avoid server crashes."""
        print(f"CRITICAL ERROR: {str(e)}")
        return jsonify({"error": "Internal Server Error", "details": str(e), "status": "error"}), 500

    return app

# Gunicorn entry point: app = create_app()
app = create_app()

if __name__ == "__main__":
    # Local dev runner
    port = int(os.environ.get("PORT", 5000))
    print(f"== Starting Vynote Production AI Backend on port {port} ==")
    app.run(host="0.0.0.0", port=port, debug=False)
