from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
import os

app = Flask(__name__)
CORS(app)

openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/", methods=["GET"])
def health_check():
    return jsonify({"status": "Service is up and running!"})

@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()
    question = data.get("message", "")

    allowed_keywords = ["off-road", "offroading", "dune", "sand", "4x4", "recovery", "trail", "vehicle", "gear", "terrain", "deflation"]
    if not any(keyword in question.lower() for keyword in allowed_keywords):
        return jsonify({"reply": "Sorry, I can only help with off-roading topics."})

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            max_tokens=100,
            messages=[
                {"role": "system", "content": "You are an expert off-road driving assistant. Only respond to topics about off-roading."},
                {"role": "user", "content": question}
            ]
        )
        reply = response.choices[0].message["content"]
        return jsonify({"reply": reply})

    except Exception as e:
        return jsonify({"reply": f"Error: {str(e)}"}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
