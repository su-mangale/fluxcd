import json
import re
import os
import random
from pathlib import Path

# Load FAQ data from JSON file
def load_faq_data():
    data_path = Path(__file__).parent / 'data' / 'faqs.json'
    try:
        with open(data_path, 'r') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        # Return empty data if file doesn't exist or is invalid
        return {"faqs": []}

# Clean and normalize text for better matching
def normalize_text(text):
    # Convert to lowercase and remove punctuation
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)
    return text

# Find the best matching FAQ based on keyword matching
def find_best_match(user_input, faqs):
    user_input = normalize_text(user_input)
    best_match = None
    highest_score = 0
    
    for faq in faqs:
        # Check each keyword in the FAQ's keywords list
        score = 0
        for keyword in faq.get('keywords', []):
            if normalize_text(keyword) in user_input:
                score += 1
                
        # Also check if any part of the question matches
        question = normalize_text(faq.get('question', ''))
        words = question.split()
        for word in words:
            if len(word) > 3 and word in user_input:  # Only match significant words
                score += 0.5
                
        if score > highest_score:
            highest_score = score
            best_match = faq
    
    return best_match, highest_score

# Main function to get response for user input
def get_response(user_input):
    faq_data = load_faq_data()
    faqs = faq_data.get('faqs', [])
    
    # Handle greetings
    greetings = ['hi', 'hello', 'hey', 'greetings']
    if normalize_text(user_input) in greetings or any(greeting in normalize_text(user_input) for greeting in greetings):
        return "Hello! I'm your Smart Assistant. How can I help you today?"
    
    # Handle goodbyes
    goodbyes = ['bye', 'goodbye', 'see you', 'talk to you later']
    if any(goodbye in normalize_text(user_input) for goodbye in goodbyes):
        return "Goodbye! Feel free to come back if you have more questions."
    
    # Handle thank you
    thanks = ['thank', 'thanks', 'appreciate']
    if any(thank in normalize_text(user_input) for thank in thanks):
        return "You're welcome! Is there anything else I can help you with?"
    
    # Find the best match from FAQs
    best_match, score = find_best_match(user_input, faqs)
    
    # If we have a good match, return the answer
    if best_match and score > 0:
        return best_match.get('answer', "I'm not sure about that.")
    
    # Default responses if no match found
    default_responses = [
        "I'm not sure I understand. Could you rephrase your question?",
        "I don't have information about that yet. Could you ask something else?"
    ]
    
    return random.choice(default_responses)
