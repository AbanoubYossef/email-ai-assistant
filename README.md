# Email AI Assistant

An intelligent email processing system that automatically classifies incoming emails and generates contextual replies using state-of-the-art NLP models from Hugging Face. Built with a focus on modularity, confidence-based workflows, and seamless Google Colab integration.

---

## Features

- **Email Classification**: Fine-tuned BERT model categorizes emails into `inquiry`, `spam`, `complaint`, `request`, `information`, `feedback`.
- **Confidence-Based Routing**:
  - High confidence (≥ 70%): fully automated reply.
  - Medium confidence (< 70%): draft reply for human review.
  - Spam or very low confidence: flagged without reply.
- **Automated Reply Generation**: GPT-2 generates dynamic, natural-sounding responses.
- **Google Drive Integration**: All models, datasets, and logs are stored persistently on Drive.
- **Simple CLI**: Paste an email → get classification + suggested reply.
- **Robust Error Handling**: Graceful fallbacks for missing models, short emails, or unexpected inputs.
- **Modular Codebase**: Separated modules for training, classification, reply generation, and orchestration.

---

## Tech Stack

- Python 3.8+
- Hugging Face Transformers
- PyTorch
- Google Colab (development environment)
- Google Drive (storage)
- Pandas, Scikit-learn, Evaluate

---

## Project Structure

```
email_ai_assistant/
├── src/
│   ├── classify.py           # BERT classification logic
│   ├── generate_reply.py     # GPT-2 reply generation
│   ├── handle_email.py       # Confidence-based routing
│   └── train_classifier.py   # Fine-tuning script for BERT
├── main.py                   # CLI entry point
├── requirements.txt          # Python dependencies
├── README.md                 # This file
└── drive_mount_setup.ipynb
```

---

## Setup & Installation

### 1. Clone the Repository and Open in Google Colab

```bash
git clone https://github.com/Abanoubyossef/email-ai-assistant.git
```

### 2. Mount Google Drive

```python
from google.colab import drive
drive.mount('/content/drive')
```

### 3. Set the Working Directory

```python
import os
project_root = '/content/drive/MyDrive/email_ai_assistant'
os.chdir(project_root)
print(f"Current working directory: {os.getcwd()}")
```

### 4. Install Dependencies

```bash
!pip install -r requirements.txt
```

### 5. Train the Classifier

```bash
!python src/train_classifier.py
```

### 6. Run the Assistant

```bash
!python main.py
```

---

## Example Usage

**Input:**

```
Paste email text:
Subject: Question about order #12345

I placed an order last week, #12345, and I haven't received a shipping confirmation yet.
Can you please check on the status of my order?

Thanks,
A Customer
```

**Output:**

```
Category: inquiry
Confidence: 98.48%
Suggested Reply:
  "Subject: Order #12345 Status Update

  Hi there,

  Thank you for reaching out. I've checked your order #12345 and it is currently being
  processed. You should receive a shipping confirmation within 24 hours. If you have any
  further questions, feel free to ask!

  Best regards,
  Customer Support"
```

---

## Test Scenarios

| Scenario | Behaviour |
|---|---|
| ✅ High-confidence inquiry | Email classified as `inquiry` with > 70% confidence → full auto-reply generated. |
| 🚫 Spam detection | Model classifies as `spam` → no reply generated, email is discarded. |
| ⚠️ Low confidence | Confidence < 70% → draft reply printed for human review, not sent automatically. |

These tests help ensure the AI assistant handles real-world email traffic robustly and responsibly.

---

## Advantages & Disadvantages of Hugging Face

| Advantages | Disadvantages |
|---|---|
| Full control over models and data | Steeper learning curve |
| Privacy (no external API calls) | Higher resource requirements |
| Cost-effective prototyping | More deployment complexity |
| Access to state-of-the-art models | |

---

## Troubleshooting

| Problem | Solution |
|---|---|
| `%writefile` syntax error in `.py` files | Remove magic commands; they only work in notebooks. |
| NumPy `_no_nep50_warning` attribute error | Downgrade to `numpy==1.26.4`. |
| Model not found | Ensure `GOOGLE_DRIVE_PROJECT_ROOT` is set correctly and paths use `os.path.join()`. |
| `LabelEncoder` missing | Save/load it with `pickle` alongside the model. |
| Module import errors | Add `sys.path.append(project_root)` in `main.py`. |

---

## Future Improvements

- Integrate with Gmail API for end-to-end automation.
- Fine-tune GPT-2 on email corpora for higher-quality replies.
- Build a web interface using Gradio or Streamlit.
- Add multi-language support.
- Implement a user feedback loop to improve confidence thresholds.

---

## Acknowledgments

- Built with [Hugging Face Transformers](https://huggingface.co/docs/transformers)
- Inspired by real-world email overload problems
