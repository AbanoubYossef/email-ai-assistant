from transformers import pipeline

# Load the GPT-2 model for text generation
generator = pipeline("text-generation", model="gpt2")

def auto_reply(email_text):
    """
    Generates a polite reply to an email using a text generation model.

    Args:
        email_text (str): The original email content.

    Returns:
        str: A generated polite reply.
    """
    prompt = f"Reply politely to this email: \"{email_text}\""

    # Generate the reply
    # max_length: Controls the maximum length of the generated text.
    # num_return_sequences: How many different replies to generate (we want 1).
    reply = generator(prompt, max_length=80, num_return_sequences=1)[0]["generated_text"]

    # The generated text might include the prompt itself, so we'll try to remove it.
    # This is a common heuristic; for more robust solutions, consider fine-tuning
    # or more sophisticated prompt engineering with a model designed for conversations.
    if reply.startswith(prompt):
        reply = reply[len(prompt):].strip()

    return reply