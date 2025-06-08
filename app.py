from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
import os

app = Flask(__name__)
CORS(app)

openai.api_key = os.environ.get("OPENAI_API_KEY")

@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()
    user_message = data.get("message", "")

    # Limit response only to off-road related topics
    prompt = f"You are an off-road assistant. Only answer questions related to off-roading, such as vehicle setup, desert navigation, trail recommendations, safety, recovery gear, etc. Ignore or reject any unrelated questions. Here is the user's question: {user_message}"

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an expert off-road assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=300,  # Limiting token usage for performance and cost control
            temperature=0.7,
        )

        reply = response.choices[0].message["content"]
        return jsonify({"reply": reply})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
