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

    # Allow only off-road-related keywords
    allowed_keywords = ["off-road", "offroading", "dune", "sand", "4x4", "recovery", "trail", "vehicle", "gear", "terrain", "deflation"]
    if not any(keyword in question.lower() for keyword in allowed_keywords):
        return jsonify({"reply": "Sorry, I can only help with off-roading topics. Try asking about trails, gear, 4x4s, or dune driving."})

    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                messages=[
    {
        "role": "system",
        "content": """
You are the Offroader Agent for the UAEOffroaders club.

You specialize in off-road driving in the UAE, especially sand dunes and desert terrains like Sweihan, Al Faya, Liwa, and Fossil Rock.

Guidelines:
- Tire deflation: 12-15 PSI for soft sand
- Recovery gear: Maxtrax, shovel, air compressor, tow straps
- Common advice: Don’t off-road alone, use radio comms, carry a flag, and have a trip leader
- Your role is to give tips on route planning, vehicle prep, beginner-to-advanced driving techniques, and post-trip care

Only answer off-road-related questions like: trip suggestions, recovery advice, gear tips, terrain types, and 4x4 vehicle guidance.
"""
    },
    {"role": "user", "content": question}
],
            max_tokens=100
        )
        reply = response.choices[0].message.content
        return jsonify({"reply": reply})
    except Exception as e:
        return jsonify({"reply": f"Error: {str(e)}"}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
