from datasets import load_dataset
from transformers import BartTokenizer, BartForConditionalGeneration, Trainer, TrainingArguments

# Load the dataset
dataset = load_dataset("cnn_dailymail", "3.0.0")

# Define preprocessing function
def preprocess_function(examples):
    return {'text': examples['article'], 'summary': examples['highlights']}

# Apply preprocessing to all splits of the dataset
summarization_data = dataset.map(preprocess_function, batched=True)

# Load a pretrained tokenizer and model
tokenizer = BartTokenizer.from_pretrained("facebook/bart-large-cnn")
model = BartForConditionalGeneration.from_pretrained("facebook/bart-large-cnn")

# Tokenize the data for input to the model
def tokenize_function(examples):
    # Tokenize the input and output texts with the tokenizer
    model_inputs = tokenizer(examples['text'], max_length=1024, truncation=True, padding="max_length")
    with tokenizer.as_target_tokenizer():
        labels = tokenizer(examples['summary'], max_length=130, truncation=True, padding="max_length")
    model_inputs["labels"] = labels["input_ids"]
    return model_inputs

# Apply the tokenization to the dataset
tokenized_data = summarization_data.map(tokenize_function, batched=True)

# Set up training arguments
training_args = TrainingArguments(
    output_dir="./results",
    evaluation_strategy="epoch",
    per_device_train_batch_size=2,
    per_device_eval_batch_size=2,
    num_train_epochs=3,
    save_steps=500,
    save_total_limit=2,
    logging_dir="./logs"
)

# Initialize the Trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_data['train'],
    eval_dataset=tokenized_data['validation'],  # Using validation split for evaluation
)

# Train the model
trainer.train()

# Save the trained model and tokenizer
model.save_pretrained("./saved_model")
tokenizer.save_pretrained("./saved_model")
