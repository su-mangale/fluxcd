import unittest
import sys
import os
import json
from pathlib import Path

# Add the parent directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.chatbot import get_response, normalize_text, find_best_match

class TestChatbot(unittest.TestCase):
    def setUp(self):
        # Create a temporary test FAQ data
        self.test_faqs = {
            "faqs": [
                {
                    "question": "What are the admission requirements?",
                    "answer": "Our college requires a high school diploma or GED.",
                    "keywords": ["admission", "requirements", "apply"]
                },
                {
                    "question": "How much is the tuition?",
                    "answer": "Tuition is $10,000 per semester.",
                    "keywords": ["tuition", "cost", "fee", "price"]
                }
            ]
        }
    
    def test_normalize_text(self):
        # Test text normalization
        self.assertEqual(normalize_text("Hello, World!"), "hello world")
        self.assertEqual(normalize_text("What's the TUITION?"), "whats the tuition")
    
    def test_find_best_match(self):
        # Test exact keyword match
        match, score = find_best_match("What are the admission requirements?", self.test_faqs["faqs"])
        self.assertEqual(match["question"], "What are the admission requirements?")
        
        # Test partial keyword match
        match, score = find_best_match("Tell me about applying", self.test_faqs["faqs"])
        self.assertEqual(match["question"], "What are the admission requirements?")
        
        # Test with no match
        match, score = find_best_match("Where is the cafeteria?", self.test_faqs["faqs"])
        self.assertIsNone(match)
    
    def test_get_response_greeting(self):
        # Test greeting response
        response = get_response("Hello")
        self.assertIn("Hello", response)
    
    def test_get_response_goodbye(self):
        # Test goodbye response
        response = get_response("Goodbye")
        self.assertIn("Goodbye", response)
    
    def test_get_response_thanks(self):
        # Test thank you response
        response = get_response("Thank you")
        self.assertIn("welcome", response.lower())

if __name__ == '__main__':
    unittest.main()
