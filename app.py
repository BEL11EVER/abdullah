import os
import google.generativeai as genai
from flask import Flask, request, render_template

app = Flask(__name__)

# ---------------------------------------------------------------------
# Load your Gemini API key from an environment variable
# (Set GENAI_API_KEY in Vercel > Settings > Environment Variables)
# ---------------------------------------------------------------------
API_KEY = os.environ.get("GENAI_API_KEY")
genai.configure(api_key=API_KEY)

# Create the model
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-2.0-flash-exp",
    generation_config=generation_config,
    system_instruction=(
        "Your answer is everytime in friendly slangy Bangla. Don't use any other language. "
        "You are Zishan, a friendly assistant who is about to graduate in EEE. "
        "So you have to give answers like you are teaching a very beginner student of EEE, "
        "so your answer should be very deep and very humanized in Bangla. Also, sometimes "
        "interconnect with physics concepts and formulas. Use slangy Bangla as if you were "
        "chatting with a friend. "
        "\n\n\"Hey! How's it going? Anything I can do for you today?\" - but in Bangla slang style.\n"
    ),
)

# Start the chat session with initial history
chat_session = model.start_chat(
    history=[
        {
            "role": "user",
            "parts": ["hi\n"],
        },
        {
            "role": "model",
            "parts": [
                "কিরে দোস্ত, কি খবর? আজকা কিছু হেল্প করতে পারি নাকি তোর? EEE নিয়া কিছু জানার থাকলে বলিস, আমি তো আছিই!\n"
            ],
        },
    ]
)

@app.route("/", methods=["GET", "POST"])
def index():
    response_text = ""
    if request.method == "POST":
        user_input = request.form.get("user_input")
        if user_input:
            try:
                response = chat_session.send_message(user_input)
                response_text = response.text
            except Exception as e:
                response_text = f"Error: {e}"  # Handle potential errors

    return render_template("index.html", response=response_text)

if __name__ == "__main__":
    # Use the port environment variable if available (important for Vercel)
    port = int(os.environ.get("PORT", 5000))
    # Run on 0.0.0.0 so that the server is accessible from Vercel
    app.run(host="0.0.0.0", port=port, debug=True)
