from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
import os

app = Flask(__name__)
CORS(app)

# Set your OpenAI API key
openai.api_key = os.environ.get("OPENAI_API_KEY") or "your-openai-api-key-here"

@app.route('/ask', methods=['POST'])
def ask():
    try:
        data = request.get_json()
        user_question = data.get('message', '')

        # Build the prompt to keep it on-topic
        prompt = f"""You are an expert off-road assistant. ONLY answer off-road related questions.
User: {user_question}
Assistant:"""

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            max_tokens=150,
            temperature=0.7,
            messages=[
                {"role": "system", "content": "You are a helpful off-road assistant who only responds to off-roading topics."},
                {"role": "user", "content": prompt}
            ]
        )

        reply = response['choices'][0]['message']['content'].strip()
        return jsonify({'reply': reply})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000, host='0.0.0.0')
