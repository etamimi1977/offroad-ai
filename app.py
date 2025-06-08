from flask import Flask, request, jsonify
import openai
import os

app = Flask(__name__)
openai.api_key = os.environ.get('OPENAI_API_KEY')

@app.route('/ask', methods=['POST'])
def ask_ai():
    data = request.get_json()
    user_message = data.get('message', '')

    # Modified system prompt to restrict GPT to off-road topics only
    system_prompt = "You are an expert off-road driving assistant. Only respond to questions related to off-roading, desert driving, 4x4 vehicles, recovery, dune bashing, camping, gear, terrain, etc. If a question is not about off-roading, politely reply: 'Sorry, I only answer off-road related questions.'"

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message}
        ],
        max_tokens=150,  # Limit response length
        temperature=0.7   # Keep it informative but not too wild
    )

    reply = response['choices'][0]['message']['content']
    return jsonify({'reply': reply})
