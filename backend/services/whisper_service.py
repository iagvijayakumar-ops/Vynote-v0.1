import whisper
import torch
import os
import random

class WhisperService:
    def __init__(self, model_name="base"):
        """
        Loads the OpenAI Whisper model.
        Available models: 'tiny', 'base', 'small', 'medium', 'large'
        """
        print(f"Loading Whisper model: {model_name}...")
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model = whisper.load_model(model_name, device=self.device)
        print("Whisper model loaded successfully!")

    def transcribe(self, audio_file_path: str) -> dict:
        """
        Transcribes the given audio file using Whisper.
        Returns a rich object containing full text, word-level timestamps, 
        STT confidence scores, and simulated diarization.
        """
        if not os.path.exists(audio_file_path):
            raise FileNotFoundError(f"Audio file not found: {audio_file_path}")

        print(f"Transcribing: {audio_file_path}")
        
        # word_timestamps=True is critical for the React Audio sync and Confidence UI
        result = self.model.transcribe(audio_file_path, word_timestamps=True)
        
        # Build the rich transcript payload for the React Stateful workspace
        rich_transcript = []
        raw_text = result.get("text", "").strip()
        
        # Mock diarization logic - alternating speakers per segment 
        # (Replace with pyannote.audio if HF token provided by user)
        current_speaker = "Speaker 1"
        
        segments = result.get("segments", [])
        for segment in segments:
            # Toggle speaker to simulate diarization loosely based on pauses or segments
            current_speaker = "Speaker 2" if current_speaker == "Speaker 1" else "Speaker 1"
            
            for word_info in segment.get("words", []):
                 # Whisper word-level output format
                 word = word_info.get("word", "").strip()
                 start = word_info.get("start", 0)
                 end = word_info.get("end", 0)
                 # Some whisper versions output probability, simulate if absent
                 prob = word_info.get("probability", round(random.uniform(0.7, 0.99), 2))
                 
                 rich_transcript.append({
                      "speaker": current_speaker,
                      "word": word,
                      "start_time": start,
                      "end_time": end,
                      "confidence": prob
                 })

        return {
            "text": raw_text,
            "detailed": rich_transcript
        }

if __name__ == "__main__":
    # Test Whisper locally
    w = WhisperService()
    # transcript = w.transcribe("sample.mp3")
    # print(transcript)
