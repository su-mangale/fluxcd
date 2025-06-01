# Smart Chatbot

A simple, rule-based chatbot for answering college-related questions. This project demonstrates how to build a basic chatbot without using complex AI models or libraries.

## Features

- Pattern matching and keyword-based responses
- Simple and intuitive chat interface
- Pre-loaded FAQ database for common college questions
- Easy to extend with new questions and answers

## Technology Stack

- **Backend**: Python + Flask
- **Frontend**: HTML, CSS, JavaScript
- **Algorithm**: Pattern Matching, Dictionary Lookup
- **Storage**: JSON
- **Version Control**: Git

## Project Structure

```plaintext
ai-bot/
├── app/                         # Main application package
│   ├── __init__.py              # Initializes Flask app
│   ├── routes.py                # Flask routes (API endpoints)
│   ├── chatbot.py               # Core chatbot logic (rule-based)
│   └── data/                    
│       └── faqs.json            # FAQ data (questions & answers)
│
├── static/                      # Static files (CSS, JS, images)
│   └── style.css                # Basic styles for UI
│
├── templates/                   # HTML templates (Jinja2)
│   └── index.html               # Chat UI page
│
├── tests/                       # Optional: test scripts
│   └── test_chatbot.py          # Unit tests for chatbot logic
│
├── run.py                       # Main Flask runner script
├── requirements.txt             # Python dependencies
└── README.md                    # Project overview and setup guide
```

## Setup Instructions

1. Clone the repository:
   ```
   git clone https://github.com/LinuxNerdBTW/ai-bot.git
   cd ai-bot
   ```

3. Create a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

4. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

5. Run the application:
   ```
   python run.py
   ```

6. Open your browser and navigate to:
   ```
   http://127.0.0.1:5000/
   ```

## Customizing the Chatbot

### Adding New FAQs

To add new questions and answers, edit the `app/data/faqs.json` file. Each FAQ should include:

- `question`: The question text
- `answer`: The response text
- `keywords`: An array of keywords that trigger this response

Example:
```json
{
  "question": "What clubs are available??",
  "answer": "We have over 50 student clubs including debate, robotics, and photography.",
  "keywords": ["club", "organization", "activity", "extracurricular"]
}
```

### Modifying Chatbot Logic

The core chatbot logic is in `app/chatbot.py`. You can modify the pattern matching algorithm, add new response types, or implement more sophisticated text processing.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
