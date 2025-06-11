
from flask import Flask, request, jsonify
import os
from google import genai
from google.genai import types

app = Flask(__name__)

genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
model = "gemini-2.5-pro-preview-06-05"

@app.route("/ask-agent", methods=["POST"])
def ask_agent():
    user_input = request.json.get("message", "")
    if not user_input:
        return jsonify({"error": "Message is required"}), 400

    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(text=user_input),
            ],
        )
    ]
    generate_content_config = types.GenerateContentConfig(response_mime_type="text/plain")

    full_response = ""
    for chunk in genai.Client().models.generate_content_stream(
        model=model,
        contents=contents,
        config=generate_content_config,
    ):
        full_response += chunk.text

    return jsonify({"response": full_response})

if __name__ == "__main__":
    app.run(debug=True)
