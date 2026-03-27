import json
import torch
from transformers import T5Tokenizer, T5ForConditionalGeneration, Trainer, TrainingArguments
from datasets import Dataset

def train_lecture_model():
    """
    Fine-tunes a T5 model to generate structured academic notes from noisy transcripts.
    Ensures the 'Title' and 'Key Points' format is strictly followed.
    """
    print("Loading dataset...")
    # 1. Load data from dataset.json
    with open("dataset.json", "r") as f:
        data = json.load(f)

    # 2. Preprocess: Combine Instruction, Topic, and Transcript into a unified Prompt
    processed_data = []
    for item in data:
        # Prompt Engineering: A clear template helps the model learn the structure better
        prompt = (
            f"INSTRUCTION: {item['instruction']}\n"
            f"TOPIC: {item['topic']}\n"
            f"TRANSCRIPT: {item['input']}\n\n"
            f"GENERATE STRUCTURED NOTES:"
        )
        # The target MUST start with the requested symbols to teach the model formatting
        target = item["structured_notes"]
        processed_data.append({"input_text": prompt, "target_text": target})

    # Convert to HuggingFace Dataset
    hf_dataset = Dataset.from_list(processed_data)

    # 3. Model setup (Upgrade to BASE for better capacity)
    model_name = "google/flan-t5-base"
    print(f"Initializing model: {model_name}...")
    tokenizer = T5Tokenizer.from_pretrained(model_name)
    model = T5ForConditionalGeneration.from_pretrained(model_name)

    # 4. Tokenization function
    def tokenize_function(examples):
        model_inputs = tokenizer(examples["input_text"], max_length=512, truncation=True, padding="max_length")
        with tokenizer.as_target_tokenizer():
            labels = tokenizer(examples["target_text"], max_length=256, truncation=True, padding="max_length")
        model_inputs["labels"] = labels["input_ids"]
        return model_inputs

    tokenized_dataset = hf_dataset.map(tokenize_function, batched=True).shuffle(seed=42)

    # 5. Training Arguments
    training_args = TrainingArguments(
        output_dir="./models/lecture-model",
        num_train_epochs=20, # Higher epochs for better memorization of the structure
        per_device_train_batch_size=4,
        save_total_limit=2,
        logging_steps=5,
        learning_rate=5e-5, # Slightly lower LR for base model stability
        weight_decay=0.01,
        push_to_hub=False,
        report_to="none" 
    )

    # 6. Initialize Trainer
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=tokenized_dataset,
    )

    # 7. Start Training
    print("Starting training locally...")
    trainer.train()

    # 8. Save the final model and tokenizer
    print("Saving model to ./models/lecture-notes-v1")
    model.save_pretrained("./models/lecture-notes-v1")
    tokenizer.save_pretrained("./models/lecture-notes-v1")
    print("Model ready!")

if __name__ == "__main__":
    # Ensure the models directory exists
    import os
    os.makedirs("./models", exist_ok=True)
    train_lecture_model()
