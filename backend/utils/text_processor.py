import re

class TextProcessor:
    def __init__(self):
        """
        Initializes the text cleaning utility.
        """
        # List common fillers to remove
        self.fillers = [r'\buh\b', r'\bum\b', r'\ber\b', r'\bah\b', r'\blike\b', r'\byou know\b']

    def clean_transcript(self, text: str):
        """
        Basic NLP cleanup for raw speech-to-text.
        """
        if not text:
            return ""

        # Lowercase for uniform processing (optional, depends on model quality)
        # text = text.lower() # Skip lowercase for high-quality Whisper output

        # Remove fillers
        for filler in self.fillers:
            text = re.sub(filler, '', text, flags=re.IGNORECASE)

        # Fix spacing
        text = re.sub(r'\s+', ' ', text).strip()

        # Simple sentence-level cleanup
        # For example, ensuring proper punctuation if it's missing (though Whisper is usually good)
        # We can add more advanced regex rules here if needed.

        # Capitalize first letter of every sentence
        # text = '. '.join([s.strip().capitalize() for s in text.split('.')])

        return text

if __name__ == "__main__":
    tp = TextProcessor()
    raw = "uh, so like, the quantum physics is um... very complex you know."
    print(tp.clean_transcript(raw))
