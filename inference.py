import torch
from transformers import T5Tokenizer, T5ForConditionalGeneration

def run_inference(topic: str, lecture: str, model_path: str = "./models/lecture-notes-v1"):
    """
    Runs inference on a noisy transcript to generate structured notes.
    Using the trained model's specific prompt format.
    """
    print(f"Loading trained model from: {model_path}...")
    tokenizer = T5Tokenizer.from_pretrained(model_path)
    model = T5ForConditionalGeneration.from_pretrained(model_path)
    model.eval()

    # Step 1: Format Prompt (Must match training)
    prompt = (
        f"INSTRUCTION: Transform lecture into structured academic notes.\n"
        f"TOPIC: {topic}\n"
        f"TRANSCRIPT: {lecture}\n\n"
        f"GENERATE STRUCTURED NOTES:"
    )

    # Step 2: Tokenize and Generate
    print("Generating structured notes...")
    inputs = tokenizer(prompt, return_tensors="pt", max_length=512, truncation=True)
    
    with torch.no_grad():
        outputs = model.generate(
            **inputs, 
            max_length=256, 
            num_beams=4, 
            no_repeat_ngram_size=3, # Prevent loops
            early_stopping=True
        )
    
    # Step 3: Decode and Format Result
    result = tokenizer.decode(outputs[0], skip_special_tokens=True)
    
    return result

if __name__ == "__main__":
    # Test with a new topic
    sample_topic = "Quantum Physics"
    sample_lecture = "so today we talk about the double slit experiment. light acts as both a wave and a particle um it's called wave-particle duality. when we observe it the wave function collapses uh into a single state. this was a huge discovery for quantum mechanics you know."
    
    try:
        notes = run_inference(sample_topic, sample_lecture)
        print("\n" + "="*50)
        print("GENERATED NOTES:")
        print("="*50)
        print(notes)
    except Exception as e:
        print(f"Inference error: {e}. (Ensure training is complete first!)")
