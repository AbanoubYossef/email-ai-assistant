import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import os

# Set random seed for reproducibility
np.random.seed(42)
random.seed(42)

# Define categories and their distribution
categories = {
    "spam": 0.20,
    "inquiry": 0.25,
    "complaint": 0.15,
    "request": 0.15,
    "information": 0.15,
    "feedback": 0.10
}

# Sample sizes
TOTAL_SAMPLES = 5000

# Names, domains and companies for more realistic emails
first_names = ["James", "Mary", "John", "Patricia", "Robert", "Jennifer", "Michael", "Linda", "William", "Elizabeth",
               "David", "Barbara", "Richard", "Susan", "Joseph", "Jessica", "Thomas", "Sarah", "Charles", "Karen",
               "Emma", "Daniel", "Olivia", "Matthew", "Sophia", "Anthony", "Isabella", "Mark", "Emily", "Donald",
               "Alex", "Chris", "Sam", "Jordan", "Taylor", "Avery", "Morgan", "Casey", "Riley", "Quinn"]

last_names = ["Smith", "Johnson", "Williams", "Jones", "Brown", "Davis", "Miller", "Wilson", "Moore", "Taylor",
              "Anderson", "Thomas", "Jackson", "White", "Harris", "Martin", "Thompson", "Garcia", "Martinez", "Robinson",
              "Clark", "Rodriguez", "Lewis", "Lee", "Walker", "Hall", "Allen", "Young", "Hernandez", "King",
              "Wright", "Lopez", "Hill", "Scott", "Green", "Adams", "Baker", "Gonzalez", "Nelson", "Carter"]

domains = ["gmail.com", "yahoo.com", "outlook.com", "hotmail.com", "aol.com", "protonmail.com", "icloud.com",
           "mail.com", "zoho.com", "yandex.com", "company.com", "business.org", "enterprise.net", "office365.com"]

companies = ["ABC Corp", "XYZ Inc", "Acme Industries", "Global Tech", "Smart Solutions", "Premier Products",
             "Innovative Systems", "Quality Goods", "Best Services", "Elite Enterprises", "Tech Wizards",
             "First Choice", "Expert Solutions", "Summit Industries", "Pinnacle Corp"]

products = ["Smartphone", "Laptop", "Tablet", "Monitor", "Keyboard", "Mouse", "Headphones", "Speaker",
            "Camera", "Printer", "Router", "External Drive", "Smart Watch", "TV", "Gaming Console",
            "Software Package", "Cloud Service", "Support Plan", "Premium Account", "Pro Subscription"]

# Helper function to generate random dates in the past 90 days
def random_date():
    days_ago = random.randint(1, 90)
    return (datetime.now() - timedelta(days=days_ago)).strftime("%Y-%m-%d")

# Helper function to generate random order numbers
def random_order():
    return f"ORD-{random.randint(100000, 999999)}"

# Helper function to generate random ticket numbers
def random_ticket():
    return f"TCKT-{random.randint(10000, 99999)}"

# Template generators for each category
def generate_spam():
    templates = [
        """SUBJECT: {attention_grabber}!!! Limited time offer!!!

Dear Sir/Madam,

Congratulations! You have been selected to receive our exclusive offer. {spam_pitch} Don't miss this opportunity!

Click here: www.{spam_domain}.com

Limited time offer! Act now before it's too late!

Best regards,
Marketing Team""",

        """SUBJECT: {first_name}, you won't believe this {product} deal!!!

ATTENTION: This is a time-sensitive offer for selected customers only!!!

{first_name}, you have been SPECIALLY SELECTED to receive our AMAZING offer on {product}!!!

{spam_pitch}!!! 100% GUARANTEED or your money back!!!

CLICK NOW: www.special-{spam_domain}.net

Hurry! Only 24 HOURS left!!!

The {company} Team""",

        """SUBJECT: RE: Your {product} - URGENT ACTION REQUIRED

Dear Customer,

Your {product} subscription is about to EXPIRE!!!

Renew now at 75% DISCOUNT and get BONUS features worth $599 FREE!!!

{spam_pitch}

To claim: www.{spam_domain}.biz

WARNING: If you don't act now, your account will be PERMANENTLY DELETED!

Security Department,
{company}""",

        """SUBJECT: Congratulations! You've been selected for our {product} giveaway

Hi there,

Great news! Your email was randomly selected in our {product} giveaway drawing.

To claim your FREE {product}, simply:
1. Visit www.{spam_domain}.info
2. Enter code: WIN-{random_order_number}
3. Pay only shipping & handling fee of $4.95

{spam_pitch}

Regards,
Prize Department""",

        """SUBJECT: Unclaimed {product} - Final Notice

FINAL NOTICE

Our records show that you have an UNCLAIMED {product} on file.

We have been trying to contact you regarding this matter. This is your LAST CHANCE to claim your {product} before we reassign it.

{spam_pitch}

Verify your eligibility: www.{spam_domain}-verification.com

Sincerely,
Customer Records Department"""
    ]

    attention_grabbers = ["Make m0ney FAST", "TRIPLE your income", "FR33 Cash", "LOSE WEIGHT NOW",
                          "WORK FROM HOME", "INSTANT approval", "AMAZING discovery", "SECRET method revealed"]

    spam_pitches = [
        f"Make ${random.randint(1000, 10000)} per week working from home with this simple trick that banks don't want you to know about",
        f"Lose {random.randint(10, 50)} pounds in just {random.randint(1, 4)} weeks with this miracle pill",
        f"Our new investment opportunity guarantees {random.randint(100, 900)}% returns in just {random.randint(30, 90)} days",
        f"This weird trick helps you make ${random.randint(500, 5000)} daily with only {random.randint(1, 5)} hours of work",
        f"Join our program and receive ${random.randint(1000, 5000)} into your account EVERY WEEK"
    ]

    spam_domains = ["get-rich-quick-scheme", "ez-money-maker", "weight-loss-miracle", "secret-wealth-system",
                    "income-booster", "instant-approval", "cash-generator", "money-multiplier"]

    template = random.choice(templates)

    return template.format(
        attention_grabber=random.choice(attention_grabbers),
        first_name=random.choice(first_names),
        product=random.choice(products),
        spam_pitch=random.choice(spam_pitches),
        spam_domain=random.choice(spam_domains),
        company=random.choice(companies),
        random_order_number=random_order() # Corrected: Call the function here
    )

def generate_inquiry():
    templates = [
        """SUBJECT: Question about {product} warranty

Hello Support Team,

I recently purchased your {product} (order #{order_number}) and I have a question about the warranty. {inquiry_question}

Could you please clarify this for me?

Thank you,
{full_name}""",

        """SUBJECT: {product} compatibility inquiry

Hi there,

I'm considering buying your {product} but I'm not sure if it's compatible with my current setup. {inquiry_question}

I would appreciate any information you can provide.

Best regards,
{full_name}
{email}""",

        """SUBJECT: Question regarding {product} features

Dear Sales Team,

I've been looking at your {product} online and I have some questions before making a purchase. {inquiry_question}

Also, do you offer any discounts for bulk orders?

Thanks in advance,
{full_name}""",

        """SUBJECT: Pre-purchase question

Hello,

I'm interested in your {product} but before I buy, I need to know: {inquiry_question}

I'm hoping to make a decision by {future_date}.

Regards,
{full_name}""",

        """SUBJECT: {product} information request

Dear Customer Service,

I saw your {product} advertised and I have a few questions:

1. {inquiry_question}
2. Do you ship to {location}?
3. What's the typical delivery timeframe?

Thank you for your assistance.

Sincerely,
{full_name}"""
    ]

    inquiry_questions = [
        f"The product manual states it's covered for {random.randint(1, 2)} year(s), but your website mentions a {random.randint(2, 5)}-year warranty. Which warranty period applies to my purchase?",
        f"Does this {random.choice(products)} work with {random.choice(['Windows', 'Mac', 'Linux', 'Android', 'iOS'])} devices?",
        f"Can you tell me if this product includes {random.choice(['free shipping', 'installation support', 'technical assistance', 'warranty extension'])}?",
        f"I noticed that there are different versions available. What's the difference between the Standard and Premium versions?",
        f"Is this product compatible with my existing {random.choice(['router', 'system', 'device', 'software'])}, or will I need to purchase additional components?"
    ]

    future_date = (datetime.now() + timedelta(days=random.randint(3, 14))).strftime("%B %d")
    location = random.choice(["Canada", "Europe", "Australia", "the UK", "Japan", "Mexico", "Brazil"])

    first_name = random.choice(first_names)
    last_name = random.choice(last_names)
    full_name = f"{first_name} {last_name}"
    email = f"{first_name.lower()}.{last_name.lower()}@{random.choice(domains)}"

    template = random.choice(templates)

    return template.format(
        product=random.choice(products),
        order_number=random_order(),
        inquiry_question=random.choice(inquiry_questions),
        full_name=full_name,
        email=email,
        future_date=future_date,
        location=location
    )

def generate_complaint():
    templates = [
        """SUBJECT: Disappointed with {product} purchase

Dear Customer Service,

I recently purchased your {product} (Order #{order_number}) on {purchase_date}, and I'm extremely disappointed with the quality. {complaint_detail}

I expect {resolution_request}.

Sincerely,
{full_name}""",

        """SUBJECT: Issue with recent order #{order_number}

Hello,

I'm writing to report a problem with my recent {product} purchase. {complaint_detail}

This is unacceptable, and I would like {resolution_request} as soon as possible.

Regards,
{full_name}""",

        """SUBJECT: Defective {product} - Ticket #{ticket_number}

To whom it may concern,

I bought a {product} from your company last {time_period}, and it has developed a serious fault. {complaint_detail}

I have already tried {troubleshooting_step} without success. I expect {resolution_request} immediately.

{full_name}
{phone_number}""",

        """SUBJECT: Poor customer service experience

Management Team,

I'm writing to express my dissatisfaction with the service I received regarding my {product}. {complaint_detail}

This level of service is below what I expect from your company. I'm requesting {resolution_request}.

Disappointed customer,
{full_name}""",

        """SUBJECT: Billing discrepancy for {product}

Billing Department,

I've noticed a discrepancy in my bill for the {product} I purchased on {purchase_date}. {complaint_detail}

Please review this matter and {resolution_request}.

Thank you,
{full_name}"""
    ]

    complaint_details = [
    f"The product stopped working after only {random.randint(1, 30)} days of normal use.",
    "When I opened the package, I found that " + random.choice(['parts were missing', 'it was damaged', "it wasn't what I ordered", 'the color was different from what was advertised']) + ".", # NO F-STRING for this part, use concatenation
    f"I was charged {random.choice(['twice', '$50 more than the advertised price', 'for express shipping but it arrived late'])}.",
    f"Your customer service representative was {random.choice(['rude', 'unhelpful', 'unable to answer basic questions'])} when I called for assistance.",
    "The product does not match the description on your website. Specifically, " + random.choice(['it lacks features that were advertised', 'the quality is much lower than shown', 'the dimensions are incorrect', "it doesn't perform as promised"]) + "." # NO F-STRING for this part
]
    resolution_requests = [
        "a full refund",
        "a replacement product",
        "to speak with a manager",
        "compensation for the inconvenience",
        "an explanation and apology"
    ]

    troubleshooting_steps = [
        "resetting the device",
        "following the troubleshooting guide",
        "contacting technical support",
        "reinstalling the software",
        "replacing the batteries"
    ]

    time_periods = ["week", "month", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]

    first_name = random.choice(first_names)
    last_name = random.choice(last_names)
    full_name = f"{first_name} {last_name}"
    phone_number = f"({random.randint(100, 999)}) {random.randint(100, 999)}-{random.randint(1000, 9999)}"

    template = random.choice(templates)

    return template.format(
        product=random.choice(products),
        order_number=random_order(),
        purchase_date=random_date(),
        complaint_detail=random.choice(complaint_details),
        resolution_request=random.choice(resolution_requests),
        full_name=full_name,
        ticket_number=random_ticket(),
        time_period=random.choice(time_periods),
        troubleshooting_step=random.choice(troubleshooting_steps),
        phone_number=phone_number
    )

def generate_request():
    templates = [
        """SUBJECT: Request for {product} information

Hello,

I would like to request detailed information about your {product}. {request_detail}

Please send this information to {email} by {deadline_date} if possible.

Thank you,
{full_name}""",

        """SUBJECT: Documentation request for {product}

Technical Support Team,

Could you please provide me with {request_detail} for the {product} I purchased (Order #{order_number})?

This is needed for {reason}.

Best regards,
{full_name}""",

        """SUBJECT: Request for assistance with {product}

Support Team,

I need help with my {product}. {request_detail}

I'm available for a call between {time_range} on {available_day}.

Thank you,
{full_name}
{phone_number}""",

        """SUBJECT: Special request regarding Order #{order_number}

Dear Customer Service,

I'm writing regarding my recent {product} order. {request_detail}

I understand this might be an unusual request, but I would greatly appreciate your help.

Sincerely,
{full_name}""",

        """SUBJECT: Request for {product} return/exchange

Returns Department,

I would like to {return_or_exchange} the {product} I purchased on {purchase_date} (Order #{order_number}). {request_detail}

Please let me know the next steps.

Regards,
{full_name}"""
    ]

    request_details = [
        f"Could you send me a copy of the user manual in {random.choice(['PDF format', 'English', 'Spanish', 'digital format'])}?",
        f"I need a detailed specification sheet for {random.choice(['integration purposes', 'my records', 'compatibility verification'])}.",
        f"I'm having trouble {random.choice(['setting up the device', 'connecting to WiFi', 'installing the software', 'activating my account'])} and need step-by-step instructions.",
        f"Can you provide me with {random.choice(['a replacement power cord', 'additional access codes', 'an extended warranty option', 'installation support'])}?",
        f"Would it be possible to {random.choice(['change my shipping address', 'expedite my delivery', 'add another item to my existing order', 'request a specific delivery date'])}?"
    ]

    reasons = [
        "a project I'm working on",
        "tax purposes",
        "insurance documentation",
        "my technical team",
        "compliance requirements"
    ]

    return_or_exchange = ["return", "exchange"]

    first_name = random.choice(first_names)
    last_name = random.choice(last_names)
    full_name = f"{first_name} {last_name}"
    email = f"{first_name.lower()}.{last_name.lower()}@{random.choice(domains)}"
    phone_number = f"({random.randint(100, 999)}) {random.randint(100, 999)}-{random.randint(1000, 9999)}"

    deadline_date = (datetime.now() + timedelta(days=random.randint(3, 14))).strftime("%B %d")
    time_range = f"{random.randint(9, 11)}am-{random.randint(1, 5)}pm"
    available_days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]

    template = random.choice(templates)

    return template.format(
        product=random.choice(products),
        request_detail=random.choice(request_details),
        email=email,
        deadline_date=deadline_date,
        full_name=full_name,
        order_number=random_order(),
        reason=random.choice(reasons),
        time_range=time_range,
        available_day=random.choice(available_days),
        phone_number=phone_number,
        return_or_exchange=random.choice(return_or_exchange),
        purchase_date=random_date()
    )

def generate_information():
    templates = [
        """SUBJECT: {product} order confirmation #{order_number}

Dear {first_name} {last_name},

Thank you for your order of {product} (Order #{order_number}).

{information_detail}

If you have any questions, please contact our customer service team.

Best regards,
{company} Order Department""",

        """SUBJECT: Important information about your {product}

Hello {first_name},

We're reaching out to provide important information regarding your {product}. {information_detail}

No action is required on your part at this time.

Sincerely,
{company} Product Team""",

        """SUBJECT: {product} shipping notification

Dear Customer,

We're pleased to inform you that your {product} order (#{order_number}) has been shipped. {information_detail}

You can track your package using this tracking number: {tracking_number}.

Thank you for shopping with us!

The {company} Shipping Team""",

        """SUBJECT: {product} software update available

{first_name},

A new software update is available for your {product}. {information_detail}

To download the update, please visit our support website or use the device's update feature.

Technical Support
{company}""",

        """SUBJECT: Your {product} warranty information

Dear {full_name},

This email contains important information about your {product} warranty. {information_detail}

Please save this email for your records.

Customer Care Team
{company}"""
    ]

    information_details = [
        f"Your order has been processed and is expected to ship on {(datetime.now() + timedelta(days=random.randint(1, 5))).strftime('%B %d')}. The estimated delivery date is {(datetime.now() + timedelta(days=random.randint(5, 14))).strftime('%B %d')}.",
        f"We've updated our {random.choice(['terms of service', 'privacy policy', 'user agreement', 'return policy'])} effective {(datetime.now() + timedelta(days=random.randint(10, 30))).strftime('%B %d, %Y')}. You can review the changes on our website.",
        f"The latest update includes {random.choice(['bug fixes', 'security enhancements', 'new features', 'performance improvements'])} that will enhance your experience.",
        f"Your warranty is valid until {(datetime.now() + timedelta(days=random.randint(365, 730))).strftime('%B %d, %Y')}. It covers {random.choice(['parts and labor', 'manufacturing defects', 'hardware issues', 'all components except batteries'])}.",
        f"Our office will be closed for {random.choice(['maintenance', 'a company event', 'the holidays', 'inventory'])} from {(datetime.now() + timedelta(days=random.randint(10, 20))).strftime('%B %d')} to {(datetime.now() + timedelta(days=random.randint(21, 30))).strftime('%B %d')}."
    ]

    first_name = random.choice(first_names)
    last_name = random.choice(last_names)
    full_name = f"{first_name} {last_name}"
    company = random.choice(companies)
    tracking_number = f"{random.choice(['UPS', 'FedEx', 'USPS', 'DHL'])}-{random.randint(1000000000, 9999999999)}"

    template = random.choice(templates)

    return template.format(
        product=random.choice(products),
        order_number=random_order(),
        first_name=first_name,
        last_name=last_name,
        information_detail=random.choice(information_details),
        company=company,
        tracking_number=tracking_number,
        full_name=full_name
    )

def generate_feedback():
    templates = [
        """SUBJECT: Feedback on my recent {product} purchase

Hello,

I recently purchased your {product} and wanted to share my feedback. {feedback_detail}

Overall rating: {rating}/5

Regards,
{full_name}""",

        """SUBJECT: My experience with your {product}

Customer Feedback Team,

I've been using your {product} for {time_period} now, and I wanted to let you know about my experience. {feedback_detail}

{additional_comment}

Best,
{full_name}""",

        """SUBJECT: {product} review

To {company} Team,

Here's my review of the {product} I purchased on {purchase_date}:

{feedback_detail}

Strengths: {strengths}
Areas for improvement: {improvements}

Thank you for considering my feedback.

{full_name}""",

        """SUBJECT: Thoughts on your {product}

Hi there,

I thought I'd share my thoughts on the {product} I recently bought. {feedback_detail}

Would I recommend it to others? {recommendation}

{full_name}""",

        """SUBJECT: {rating}/5 stars - {product} feedback

Feedback Department,

I'm writing in response to your request for feedback on my recent {product} purchase.

{feedback_detail}

What I liked most: {strength}
What could be improved: {improvement}

{full_name}"""
    ]

    positive_feedback = [
        f"I'm extremely impressed with the {random.choice(['quality', 'design', 'functionality', 'ease of use'])}. It exceeded my expectations in every way.",
        f"This is one of the best purchases I've made. The {random.choice(['performance', 'customer service', 'value', 'features'])} is outstanding.",
        f"I absolutely love this product! It's {random.choice(['exactly what I needed', 'beautifully designed', 'incredibly user-friendly', 'perfect for my needs'])}."
    ]

    negative_feedback = [
        f"Unfortunately, I'm disappointed with the {random.choice(['quality', 'performance', 'durability', 'customer support'])}. It fell short of my expectations.",
        f"I've encountered several issues with this product. The {random.choice(['setup process was complicated', 'materials feel cheap', 'battery life is poor', 'software is buggy'])}.",
        f"This product did not meet my needs. The {random.choice(['design is impractical', 'features are limited', 'price is too high for what you get', 'instructions were confusing'])}."
    ]

    mixed_feedback = [
        f"I have mixed feelings about this product. While the {random.choice(['design', 'performance', 'features', 'quality'])} is good, the {random.choice(['price', 'customer service', 'durability', 'user interface'])} could be improved.",
        f"There are both pros and cons to this product. I like the {random.choice(['functionality', 'appearance', 'ease of installation', 'reliability'])}, but I'm not satisfied with the {random.choice(['cost', 'material quality', 'technical support', 'size'])}.",
        random.choice(["It's good for beginners but limiting for experts", "It handles simple tasks well but struggles with complex ones", "The basic features are solid but premium features are lacking", "It works as advertised but doesn't offer anything exceptional"]) # Corrected: use double quotes for inner strings with apostrophes
    ]

    additional_comments = [
        "I hope this feedback helps you improve your products.",
        "I would love to see these improvements in future versions.",
        "Despite my concerns, I'm still a fan of your company.",
        "I've already recommended this product to several friends.",
        "I'm looking forward to trying more products from your line."
    ]

    strengths = [
        "design, ease of use, quick setup",
        "quality construction, reliable performance, good value",
        "excellent customer service, fast shipping, detailed instructions",
        "innovative features, compatibility, energy efficiency",
        "portability, modern design, intuitive controls"
    ]

    improvements = [
        "battery life, customer support, packaging",
        "price point, warranty coverage, accessory options",
        "software interface, update frequency, documentation",
        "durability, noise level, size options",
        "connectivity issues, setup complexity, weight"
    ]

    recommendations = ["Yes, definitely", "Yes, with some reservations", "Only for specific users", "Not at this time", "Yes, if certain improvements are made"]

    ratings = list(range(1, 6))  # 1-5 star ratings

    time_periods = [f"{random.randint(1, 11)} weeks", f"{random.randint(1, 12)} months", "several days", "about a week", "a few months"]

    first_name = random.choice(first_names)
    last_name = random.choice(last_names)
    full_name = f"{first_name} {last_name}"

    template = random.choice(templates)

    # Weight the feedback types
    feedback_options = []
    for _ in range(5):  # More weight to positive
        feedback_options.append(random.choice(positive_feedback))
    for _ in range(3):  # Medium weight to mixed
        feedback_options.append(random.choice(mixed_feedback))
    for _ in range(2):  # Less weight to negative
        feedback_options.append(random.choice(negative_feedback))

    feedback_detail = random.choice(feedback_options)

    # Adjust rating to match feedback sentiment
    if feedback_detail in positive_feedback:
        rating = random.choice([4, 5])
    elif feedback_detail in negative_feedback:
        rating = random.choice([1, 2])
    else:  # mixed feedback
        rating = random.choice([3, 4])

    return template.format(
        product=random.choice(products),
        feedback_detail=feedback_detail,
        rating=rating,
        full_name=full_name,
        time_period=random.choice(time_periods),
        additional_comment=random.choice(additional_comments),
        company=random.choice(companies),
        purchase_date=random_date(),
        strengths=random.choice(strengths),
        improvements=random.choice(improvements),
        recommendation=random.choice(recommendations),
        strength=random.choice(strengths).split(", ")[0],
        improvement=random.choice(improvements).split(", ")[0]
    )

# Generate emails
def generate_dataset(num_samples):
    data = []

    # Calculate samples per category
    category_samples = {}
    for category, percentage in categories.items():
        category_samples[category] = int(num_samples * percentage)

    # Adjust for rounding errors
    total_allocated = sum(category_samples.values())
    if total_allocated < num_samples:
        # Add remaining samples to largest category
        largest_category = max(category_samples, key=category_samples.get)
        category_samples[largest_category] += (num_samples - total_allocated)

    # Generate emails for each category
    for category, count in category_samples.items():
        for _ in range(count):
            if category == "spam":
                text = generate_spam()
            elif category == "inquiry":
                text = generate_inquiry()
            elif category == "complaint":
                text = generate_complaint()
            elif category == "request":
                text = generate_request()
            elif category == "information":
                text = generate_information()
            elif category == "feedback":
                text = generate_feedback()

            data.append({"text": text, "label": category})

    # Shuffle the dataset
    random.shuffle(data)

    return pd.DataFrame(data)

# ---
## Generate and Save the Dataset
# ---

df = generate_dataset(TOTAL_SAMPLES)

# Create data directory if it doesn't exist
os.makedirs("data", exist_ok=True)

# Save to CSV
df.to_csv("data/synthetic_emails.csv", index=False)

print(f"Dataset generated with {TOTAL_SAMPLES} emails.")
print(f"Distribution by category:")
print(df['label'].value_counts())

# ---
## Display Sample Emails
# ---

print("\nSample emails by category:")
for category in categories.keys():
    sample = df[df['label'] == category].sample(1).iloc[0]
    print(f"\n--- {category.upper()} SAMPLE ---")
    # Limiting output length for readability
    print(sample['text'][:300] + "..." if len(sample['text']) > 300 else sample['text'])
    print("-" * 50)