import torch
import torch.nn.functional as F
from transformers import BertTokenizer, BertForSequenceClassification
import pickle
import os

# --- IMPORTANT CHANGE: Define your Google Drive project path ---
# This path should point to the root of your 'email_ai_assistant' folder on Google Drive
GOOGLE_DRIVE_PROJECT_ROOT = "/content/drive/MyDrive/email_ai_assistant"

# Construct the absolute path to the model and tokenizer on Google Drive
model_path = os.path.join(GOOGLE_DRIVE_PROJECT_ROOT, "models", "email_classifier_model")
label_encoder_path = os.path.join(GOOGLE_DRIVE_PROJECT_ROOT, "models", "email_classifier_model", "label_encoder.pkl")


# Load model and tokenizer
try:
    model = BertForSequenceClassification.from_pretrained(model_path)
    tokenizer = BertTokenizer.from_pretrained(model_path)
except Exception as e:
    print(f"Error loading model or tokenizer from {model_path}: {e}")
    print("Please ensure the model has been trained and saved correctly.")
    raise

# Load label encoder
try:
    with open(label_encoder_path, "rb") as f:
        le = pickle.load(f)
except FileNotFoundError:
    print(f"Error: label_encoder.pkl not found at {label_encoder_path}.")
    print("Please ensure the training script saved the label encoder.")
    raise
except Exception as e:
    print(f"Error loading label encoder from {label_encoder_path}: {e}")
    raise


def classify_email(text, confidence_threshold=0.7):
    """
    Classify email with confidence score and threshold-based decision making

    Args:
        text (str): The email text to classify
        confidence_threshold (float): Minimum confidence to assign a definite category

    Returns:
        dict: Classification result with category, confidence, and need_review flag
    """
    try:
        if not text or len(text.strip()) < 10:
            return {
                "category": "unclassified",
                "confidence": 0.0,
                "need_review": True,
                "all_scores": {}
            }

        inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True)

        with torch.no_grad():
            logits = model(**inputs).logits

        # Convert logits to probabilities
        probs = F.softmax(logits, dim=1)[0]

        # Get top prediction and its probability
        top_prob, top_idx = torch.max(probs, dim=0)
        predicted_category = le.inverse_transform([top_idx.item()])[0]
        confidence = top_prob.item()

        # Get all category probabilities
        all_categories = le.classes_
        all_scores = {cat: probs[le.transform([cat])[0]].item() for cat in all_categories}

        # Determine if human review is needed based on confidence
        need_review = confidence < confidence_threshold

        return {
            "category": predicted_category,
            "confidence": confidence,
            "need_review": need_review,
            "all_scores": all_scores
        }
    except Exception as e:
        print(f"Classification error: {e}")
        return {
            "category": "error",
            "confidence": 0.0,
            "need_review": True,
            "all_scores": {}
        }

if __name__ == "__main__":
    # Example usage:
    test_emails = [
        "Dear customer, your account has been compromised. Click this link to verify.",
        "Meeting reminder for tomorrow at 10 AM regarding the project deadline.",
        "Congratulations! You've won a free vacation to the Bahamas! Claim now!",
        "Regarding your recent inquiry about the product, here's the information you requested.",
        "Short email", # Test for short/empty email handling
        "" # Test for empty email handling
    ]

    print("--- Email Classification Results ---")
    for i, email in enumerate(test_emails):
        print(f"\nEmail {i+1}: '{email}'")
        result = classify_email(email)
        print(f"  Category: {result['category']}")
        print(f"  Confidence: {result['confidence']:.4f}")
        print(f"  Needs Review: {result['need_review']}")
        print(f"  All Scores: {result['all_scores']}")