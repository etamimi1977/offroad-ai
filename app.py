from flask import Flask, request, jsonify
import os
import google.generativeai as genai
from google.generativeai import GenerativeModel
import logging

app = Flask(__name__)

# Logging setup
logging.basicConfig(level=logging.INFO)

# Set API key from environment variable
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

# Initialize model
model = GenerativeModel("gemini-pro")

@app.route("/", methods=["GET"])
def home():
    return "Gemini-powered 4x4 Bot is running!", 200

@app.route("/chat", methods=["POST"])
def chat():
    try:
        user_input = request.json.get("message", "")
        if not user_input:
            return jsonify({"error": "No message provided"}), 400

        logging.info(f"User input: {user_input}")
        response = model.generate_content(user_input)
        return jsonify({"response": response.text})
    except Exception as e:
        logging.error(f"Error: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
