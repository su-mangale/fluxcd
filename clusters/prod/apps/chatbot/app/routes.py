from flask import Blueprint, render_template, request, jsonify
from app.chatbot import get_response

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/api/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_message = data.get('message', '')
    
    if not user_message:
        return jsonify({'response': 'Please enter a message.'})
    
    bot_response = get_response(user_message)
    return jsonify({'response': bot_response})
