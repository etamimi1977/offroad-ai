from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
import os

app = Flask(__name__)
CORS(app)

openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()
    question = data.get("message", "")

    if not question:
        return jsonify({"error": "No question provided"}), 400

    # Force off-road topic
    prompt = f"You are an off-road expert. Only reply to off-roading-related questions. Ignore other topics. Question: {question}"

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an off-road expert assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=150
        )
        reply = response['choices'][0]['message']['content']
        return jsonify({"reply": reply})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))  # use 10000 or any custom port
    app.run(host="0.0.0.0", port=port)
