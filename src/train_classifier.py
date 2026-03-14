# Updated src/train_classifier.py for Google Drive paths

import pandas as pd
from datasets import Dataset, load_dataset
from transformers import (
    BertTokenizerFast,
    BertForSequenceClassification,
    TrainingArguments,
    Trainer,
    EarlyStoppingCallback
)
import numpy as np
import evaluate
from sklearn.preprocessing import LabelEncoder
import pickle
import os

# --- IMPORTANT CHANGE: Define your Google Drive project path ---
# Use your actual folder name: 'email_ai_assistant'
GOOGLE_DRIVE_PROJECT_ROOT = "/content/drive/MyDrive/email_ai_assistant"

# 1) Point to your CSV here, using the Google Drive path:
DATA_PATH = os.path.join(GOOGLE_DRIVE_PROJECT_ROOT, "data", "synthetic_emails.csv")

# 2) Load & split using Pandas first, then convert to Dataset
if not os.path.exists(DATA_PATH):
    raise FileNotFoundError(f"Data file not found at {DATA_PATH}. Please upload your CSV.")

df = pd.read_csv(DATA_PATH)
raw = Dataset.from_pandas(df)

splits = raw.train_test_split(test_size=0.2, seed=42)

# 3) Load tokenizer & model
tokenizer = BertTokenizerFast.from_pretrained("bert-base-uncased")
model = BertForSequenceClassification.from_pretrained(
    "bert-base-uncased",
    num_labels=len(raw.unique("label"))
)

# 4) Encode labels numerically
le = LabelEncoder()
labels_list = raw["label"]
le.fit(labels_list)

def encode_labels(example):
    return {'labels': le.transform([example['label']])[0]}

splits = splits.map(encode_labels)

# Save the label encoder to the models directory on Drive
output_dir = os.path.join(GOOGLE_DRIVE_PROJECT_ROOT, "models", "email_classifier_model")
os.makedirs(output_dir, exist_ok=True)
with open(os.path.join(output_dir, "label_encoder.pkl"), "wb") as f:
    pickle.dump(le, f)

label2id = {label: i for i, label in enumerate(le.classes_)}
id2label = {i: label for i, label in enumerate(le.classes_)}
model.config.label2id = label2id
model.config.id2label = id2label

# 5) Tokenization
def tokenize_fn(batch):
    return tokenizer(batch["text"], padding="max_length", truncation=True, max_length=128)

splits = splits.map(tokenize_fn, batched=True)
splits.set_format(
    type="torch",
    columns=["input_ids", "attention_mask", "labels"]
)

# 6) Metrics: accuracy
accuracy = evaluate.load("accuracy")
def compute_metrics(p):
    preds = np.argmax(p.predictions, axis=1)
    return accuracy.compute(predictions=preds, references=p.label_ids)

# 7) Training arguments
training_args = TrainingArguments(
    output_dir=output_dir,
    eval_strategy="epoch",
    save_strategy="epoch",
    load_best_model_at_end=True,
    metric_for_best_model="accuracy",
    greater_is_better=True,
    per_device_train_batch_size=8,
    per_device_eval_batch_size=8,
    num_train_epochs=3,
    logging_dir=os.path.join(GOOGLE_DRIVE_PROJECT_ROOT, "logs"), # Log dir on Drive
    logging_steps=10,
)

# 8) Trainer with EarlyStopping
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=splits["train"],
    eval_dataset=splits["test"],
    compute_metrics=compute_metrics,
    callbacks=[EarlyStoppingCallback(early_stopping_patience=2)]
)

# 9) Train model
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=splits["train"],
    eval_dataset=splits["test"],
    tokenizer=tokenizer,
    compute_metrics=compute_metrics,
    callbacks=[EarlyStoppingCallback(early_stopping_patience=3)]
)

trainer.train()

trainer.save_model(training_args.output_dir)
tokenizer.save_pretrained(training_args.output_dir)
