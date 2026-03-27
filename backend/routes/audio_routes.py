from flask import Blueprint, request, jsonify
import os
import uuid
import yt_dlp
from werkzeug.utils import secure_filename
from services.whisper_service import WhisperService

audio_bp = Blueprint('audio', __name__)

UPLOAD_FOLDER = os.path.join(os.getcwd(), 'data', 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Shared instance with HF API settings (production-ready)
whisper_service = WhisperService()

@audio_bp.route('/upload', methods=['POST'])
def upload_audio():
    """Endpoint for direct audio file upload."""
    print("AUDIO ROUTE: /upload accessed.")
    if 'file' not in request.files:
        print("AUDIO ROUTE ERROR: No file part in request.")
        return jsonify({"error": "No file part", "status": "error"}), 400
        
    file = request.files['file']
    if file.filename == '':
        print("AUDIO ROUTE ERROR: No selected file.")
        return jsonify({"error": "No selected file", "status": "error"}), 400
        
    if file:
        filename = secure_filename(file.filename)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        print(f"AUDIO ROUTE: Saving file to {filepath}")
        file.save(filepath)
        
        try:
            print("AUDIO ROUTE: Starting transcription via Hugging Face API...")
            # Use the refactored transcribe_audio method
            transcript_data = whisper_service.transcribe_audio(filepath)
            print("AUDIO ROUTE: Transcription complete.")
            
            # Cleanly handle temporary file after transcription in production
            # os.remove(filepath)
            
            # Fulfilling the requirement for 'transcription' and 'status'
            return jsonify(transcript_data), 200
        except Exception as e:
            print(f"AUDIO ROUTE Transcription Error: {str(e)}")
            return jsonify({"error": str(e), "status": "error"}), 500


@audio_bp.route('/youtube', methods=['POST'])
def fetch_youtube_audio():
    """Endpoint to download audio from a YouTube URL via yt-dlp."""
    print("AUDIO ROUTE: /youtube accessed.")
    data = request.get_json()
    if not data or 'url' not in data:
        print("AUDIO ROUTE ERROR: Missing URL.")
        return jsonify({"error": "Missing YouTube URL", "status": "error"}), 400
        
    url = data['url']
    print(f"AUDIO ROUTE: Processing YouTube URL: {url}")
    unique_id = str(uuid.uuid4())
    
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': os.path.join(UPLOAD_FOLDER, f"{unique_id}"),
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'quiet': True,
        'no_warnings': True
    }
    
    try:
        print("AUDIO ROUTE: Downloading YouTube audio via yt_dlp...")
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
            
        final_filepath = os.path.join(UPLOAD_FOLDER, f"{unique_id}.mp3")
        
        if not os.path.exists(final_filepath):
             print(f"AUDIO ROUTE ERROR: Downloaded file path expected: {final_filepath}")
             return jsonify({"error": "yt-dlp failed to find the final MP3 file.", "status": "error"}), 500

        print("AUDIO ROUTE: Starting transcription via Hugging Face API...")
        transcript_data = whisper_service.transcribe_audio(final_filepath)
        print("AUDIO ROUTE: Youtube transcription complete.")
        
        # In production, we'd clean up the large mp3 file
        # os.remove(final_filepath)
        
        return jsonify(transcript_data), 200
        
    except Exception as e:
        print(f"AUDIO ROUTE YouTube Error Tracking: {str(e)}")
        return jsonify({"error": f"Internal YouTube Processor Failure: {str(e)}", "status": "error"}), 500
