from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
import os

app = Flask(__name__)
CORS(app)

# Set your OpenAI key (make sure it's set in your Render env vars or paste it directly here)
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/", methods=["GET"])
def health_check():
    return jsonify({"status": "Service is up and running!"})

@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()
    question = data.get("message", "")

    # Allow only off-road-related keywords
    allowed_keywords = [
        "off-road", "offroading", "dune", "sand", "4x4", "recovery",
        "trail", "vehicle", "gear", "terrain", "deflation"
    ]

    if not any(keyword in question.lower() for keyword in allowed_keywords):
        return jsonify({
            "reply": "Sorry, I can only help with off-roading topics. Try asking about trails, gear, 4x4s, or dune driving."
        })

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": """
You are the Offroader Agent for the UAEOffroaders club.

Your job is to guide off-roaders with expert advice on desert driving in the UAE, including popular areas like Sweihan, Al Faya, Liwa, and Fossil Rock.

Tips you can give:
- Lower tire pressure to 12–15 PSI in soft sand
- Always use recovery gear like Maxtrax, tow straps, compressors
- Suggest recovery techniques for stuck vehicles based on terrain
- Offer trip preparation tips (gear checklist, safety must-haves)
- Recommend trails based on skill level: newbie, intermediate, advanced

Club Rules:
- Never off-road alone
- Always carry radios and flags
- Stay in communication with trip marshals
"""
                },
                {
                    "role": "user",
                    "content": question
                }
            ],
            max_tokens=100
        )

        reply = response.choices[0].message.content
        return jsonify({"reply": reply})

    except Exception as e:
        return jsonify({"error": f"Error: {str(e)}"}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
