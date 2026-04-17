import os
from flask import Flask, request, jsonify, render_template
from openai import OpenAI

app = Flask(__name__)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

chat_history = []

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message")

    messages = [
        {
            "role": "system",
            "content": "You are a smart multilingual assistant. Answer in the user's language."
        }
    ]

    for msg in chat_history[-10:]:
        messages.append(msg)

    messages.append({"role": "user", "content": user_input})

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=messages
    )

    answer = response.choices[0].message.content

    chat_history.append({"role": "user", "content": user_input})
    chat_history.append({"role": "assistant", "content": answer})

    return jsonify({"response": answer})

if __name__ == "__main__":
    app.run()