# Updated main.py
from src.handle_email import handle_email
import argparse

if __name__ == "__main__":
    # Create argument parser
    parser = argparse.ArgumentParser(description='Email Classification and Response System')
    parser.add_argument('--confidence', type=float, default=0.7,
                        help='Confidence threshold for classification (0.0-1.0)')
    parser.add_argument('--input', type=str, help='Input file with email text')
    args = parser.parse_args()
    
    # Get email text from file or prompt
    if args.input:
        try:
            with open(args.input, 'r') as f:
                email_text = f.read()
        except Exception as e:
            print(f"Error reading input file: {e}")
            exit(1)
    else:
        # Interactive mode
        email_text = input("Paste email text:\n> ")
    
    # Process the email with configured confidence threshold
    handle_email(email_text, args.confidence)