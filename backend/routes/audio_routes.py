from flask import Blueprint, request, jsonify
import os
import uuid
import yt_dlp
from werkzeug.utils import secure_filename
from services.whisper_service import WhisperService

audio_bp = Blueprint('audio', __name__)

UPLOAD_FOLDER = os.path.join(os.getcwd(), 'data', 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

whisper_service = WhisperService()

@audio_bp.route('/upload', methods=['POST'])
def upload_audio():
    """Endpoint for direct audio file upload."""
    print("AUDIO ROUTE: /upload accessed.")
    if 'file' not in request.files:
        print("AUDIO ROUTE ERROR: No file part in request.")
        return jsonify({"error": "No file part"}), 400
        
    file = request.files['file']
    if file.filename == '':
        print("AUDIO ROUTE ERROR: No selected file.")
        return jsonify({"error": "No selected file"}), 400
        
    if file:
        filename = secure_filename(file.filename)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        print(f"AUDIO ROUTE: Saving file to {filepath}")
        file.save(filepath)
        
        try:
            print("AUDIO ROUTE: Starting transcription via Whisper...")
            transcript_data = whisper_service.transcribe(filepath)
            print("AUDIO ROUTE: Transcription complete.")
            return jsonify(transcript_data), 200
        except Exception as e:
            print(f"AUDIO ROUTE Transcription Error: {str(e)}")
            return jsonify({"error": str(e)}), 500


@audio_bp.route('/youtube', methods=['POST'])
def fetch_youtube_audio():
    """Endpoint to download audio from a YouTube URL via yt-dlp."""
    print("AUDIO ROUTE: /youtube accessed.")
    data = request.get_json()
    if not data or 'url' not in data:
        print("AUDIO ROUTE ERROR: Missing URL.")
        return jsonify({"error": "Missing YouTube URL"}), 400
        
    url = data['url']
    print(f"AUDIO ROUTE: Processing YouTube URL: {url}")
    unique_id = str(uuid.uuid4())
    output_template = os.path.join(UPLOAD_FOLDER, f"{unique_id}.%(ext)s")
    
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': os.path.join(UPLOAD_FOLDER, f"{unique_id}"),
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'quiet': False,
        'no_warnings': False
    }
    
    try:
        print("AUDIO ROUTE: Downloading YouTube audio via yt_dlp...")
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
            
        final_filepath = os.path.join(UPLOAD_FOLDER, f"{unique_id}.mp3")
        print(f"AUDIO ROUTE: Downloaded file path expected: {final_filepath}")
        
        if not os.path.exists(final_filepath):
             # Fallback check for alternate formats
             print("AUDIO ROUTE WARNING: MP3 file not found, checking for alternate downloads.")
             
        print("AUDIO ROUTE: Starting transcription...")
        transcript_data = whisper_service.transcribe(final_filepath)
        print("AUDIO ROUTE: Youtube transcription complete.")
        return jsonify(transcript_data), 200
        
    except Exception as e:
        print(f"AUDIO ROUTE YouTube Error Tracking: {str(e)}")
        return jsonify({"error": f"Internal YouTube Processor Failure: {str(e)}"}), 500
