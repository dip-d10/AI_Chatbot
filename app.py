import openai
import os
from dotenv import load_dotenv
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

# Load API Key
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Initialize OpenAI client
client = openai.OpenAI(api_key=OPENAI_API_KEY)

# Create Flask app
app = Flask(__name__, static_folder="static", template_folder="templates")
CORS(app)  # Enable CORS for frontend

# Store conversation history
conversation_history = []

@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    global conversation_history
    data = request.json
    user_message = data.get("message", "")

    if not user_message:
        return jsonify({"error": "Empty message"}), 400

    # Add user message to history
    conversation_history.append({"role": "user", "content": user_message})

    # Keep only the last 10 messages (to avoid large requests)
    conversation_history = conversation_history[-10:]

    # Call OpenAI API with history
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=conversation_history
    )

    bot_reply = response.choices[0].message.content

    # Add bot reply to history
    conversation_history.append({"role": "assistant", "content": bot_reply})

    return jsonify({"reply": bot_reply})

@app.route("/clear_chat", methods=["POST"])
def clear_chat():
    global conversation_history
    conversation_history = []  # Reset memory
    return jsonify({"message": "Chat history cleared!"})

if __name__ == "__main__":
    app.run(debug=True)
