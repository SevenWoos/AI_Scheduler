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
        tasks = data.get('tasks', '').strip()
        time_available = data.get('time_available', '').strip()
        time_im_free = data.get('time_im_free', '').strip()
        schedule_preference = data.get('schedule_preference', '').strip()
        extra_notes = data.get('message', '').strip()

        # Prompt Injection
        user_input = f"""
            Tasks: {tasks}
            Time Available: {time_available}
            Time I'm Free: {time_im_free}
            Schedule Preference: {schedule_preference}
            Extra Notes: {extra_notes}
        """


        # prompt_path = os.path.join(os.path.dirname(__file__), 'prompts', 
        #                            'prompt_v1.txt')

        # prompt_path = os.path.join(os.path.dirname(__file__), 'prompts', 
        #                            'prompt_v2.txt')

        # prompt_path = os.path.join(os.path.dirname(__file__), 'prompts', 
        #                            'prompt_v3.txt')

        # prompt_path = os.path.join(os.path.dirname(__file__), 'prompts', 
        #                            'prompt_v4.txt')

        # prompt_path = os.path.join(os.path.dirname(__file__), 'prompts', 
        #                            'prompt_v5.txt')

        # prompt_path = os.path.join(os.path.dirname(__file__), 'prompts', 
        #                            'llm_scheduling_prompt_corrected.txt')

        # prompt_path = os.path.join(os.path.dirname(__file__), 'prompts', 
        #                            'llm_scheduling_prompt_corrected_v2.txt')

        prompt_path = os.path.join(os.path.dirname(__file__), 'prompts', 
                                   'prompt_v6.txt')

        # prompt_path = os.path.join(os.path.dirname(__file__), 'prompts', 
        #                            'prompt_v7.txt')
        
        
        with open(prompt_path, 'r', encoding='utf-8') as f:
            prompt_template = f.read()


        # user input match prompt
        full_prompt = prompt_template.replace('{{USER_INPUT_HERE}}', user_input)


        response = requests.post(
            'http://localhost:11434/api/generate', 
            json={
                "model": "llama3", 
                "prompt": full_prompt, 
                "stream": False
            }
        )

        data = response.json()
        return jsonify({"response": data.get("response", "")})
    
    return render_template('chat.html', user=current_user)