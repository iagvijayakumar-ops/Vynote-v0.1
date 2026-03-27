import os
os.environ["PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION"] = "python"
import sys
import os

# Add the project root to sys.path if needed
sys.path.append(os.getcwd())

try:
    print("Testing WhisperService...")
    from backend.services.whisper_service import WhisperService
    w = WhisperService()
    print("WhisperService OK.")
    
    print("\nTesting NLPService...")
    from backend.services.nlp_service import NLPService
    n = NLPService()
    print("NLPService OK.")
    
    print("\nTesting AssessmentService...")
    from backend.services.assessment_service import AssessmentService
    a = AssessmentService()
    print("AssessmentService OK.")
    
    print("\nTesting RAGService...")
    from backend.services.rag_service import RAGService
    r = RAGService()
    print("RAGService OK.")
    
    print("\nAll services initialized successfully.")
except Exception as e:
    print(f"\nCRITICAL ERROR during initialization: {e}")
    import traceback
    traceback.print_exc()
