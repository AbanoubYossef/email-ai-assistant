# Updated handle_email.py
from src.classify import classify_email
from src.generate_reply import auto_reply

def handle_email(text, confidence_threshold=0.7):
    """
    Process email with enhanced confidence-based handling
    
    Args:
        text (str): The email text to process
        confidence_threshold (float): Minimum confidence for automatic handling
    """
    try:
        if not text or not isinstance(text, str):
            print("Error: Invalid email text provided")
            return
        
        # Get classification with confidence
        result = classify_email(text, confidence_threshold)
        
        # Display results
        print(f"\n📩 Category: {result['category']}")
        print(f"🔍 Confidence: {result['confidence']:.2%}")
        
        # Show all category scores for transparency
        print("\n📊 All category scores:")
        for category, score in sorted(result['all_scores'].items(), key=lambda x: x[1], reverse=True):
            print(f"  - {category}: {score:.2%}")
        
        # Handle based on classification result
        if result['category'].lower() == "spam":
            print("\n⚠️ Spam detected - no reply generated")
        elif result['need_review']:
            print("\n⚠️ Low confidence classification - human review recommended")
            if result['confidence'] > 0.4:  # Still generate a draft if somewhat confident
                reply = auto_reply(text)
                print("\n📝 Draft Reply (NEEDS REVIEW):")
                print(reply)
        else:
            # High confidence non-spam case
            reply = auto_reply(text)
            print("\n📝 Suggested Reply:")
            print(reply)
    except Exception as e:
        print(f"Critical error in email handling: {e}")