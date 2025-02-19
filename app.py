from flask import Flask, request, jsonify, render_template
import requests

app = Flask(__name__)

# Gemini API configuration (⚠️ Do NOT hardcode API keys in production)
GEMINI_API_KEY = ""
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"

# Predefined responses with emojis
PREDEFINED_RESPONSES = {
    "hi": "Hello! 👋 How can I assist you today? 😊",
    "how are you": "I'm doing great, thanks for asking! 😄 How about you?",
    "what's your name": "I'm your friendly AI chatbot! 🤖",
    "bye": "Goodbye! 👋 Have a wonderful day! 🌟",
}

def get_gemini_response(user_input):
    """Fetch response from Gemini AI API."""
    headers = {
        "Content-Type": "application/json",
    }
    params = {"key": GEMINI_API_KEY}  # API Key in query parameters
    data = {
        "contents": [
            {"parts": [{"text": user_input}]}
        ]
    }
    
    try:
        response = requests.post(GEMINI_API_URL, headers=headers, params=params, json=data)
        response.raise_for_status()
        gemini_data = response.json()

        # Extract response from Gemini API
        candidates = gemini_data.get("candidates", [])
        if candidates:
            return candidates[0].get("content", {}).get("parts", [{}])[0].get("text", "Sorry, I couldn't process that. 😅")
        return "Sorry, I didn't understand that. 🤖"

    except requests.exceptions.RequestException as e:
        print(f"Error calling Gemini API: {e}")
        return "Oops! Something went wrong. Please try again later. 😅"

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message", "").strip().lower()
    response = PREDEFINED_RESPONSES.get(user_input, None)

    if not response:
        # Fallback to Gemini AI for unknown queries
        response = get_gemini_response(user_input)

    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(debug=True)
