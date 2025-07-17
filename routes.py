from flask import render_template, request, redirect, url_for, session, jsonify,Blueprint
from flask_login import login_required, current_user
import requests
import os


chat_bp = Blueprint('chat', __name__)

@chat_bp.route('/chat', methods=['GET', 'POST'])
@login_required
def chat():
    if request.method == 'POST':
        data = request.get_json()

        # Fields


        # Prompt Injection
        user_input = f"""

        """


        prompt_path = os.path.join(os.path.dirname(__file__), 'prompts', 
                                   'prompt_v1.txt')
        
        with open(prompt_path, 'r', encoding='utf-8') as f:
            prompt_template = f.read()


        # user input match prompt
        full_prompt = prompt_template.replace('{{USER_INPUT_HERE}}', user_input)


        response = requests.post(
            'https://localhost:11434/api/generate', 
            json={
                "model": "llama3", 
                "prompt": full_prompt, 
                "stream": False
            }
        )

        data = response.json()
        return jsonify({"response": data.get("response", "")})
    
    return render_template('chat.html', user=current_user)