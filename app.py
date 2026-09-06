"""
AI Chat Widget Demo — Trattoria Bella Vista
---------------------------------------------
A tiny Flask backend that powers an AI chat widget for a local restaurant.
The widget answers customer questions (hours, menu, reservations, allergens)
using only the info you give it in BUSINESS_CONTEXT below — no hallucinated
menu items, no made-up hours.

This is meant as a portfolio / cold-outreach demo: swap BUSINESS_CONTEXT for
a real client's info and you have a sellable product in minutes.

Setup:
    pip install -r requirements.txt
    export GEMINI_API_KEY="AQ.Ab8RN6Jk2pvxBJLdX_rKLPIdjBahdCW94duDiV3ELFXQlAj_6Q"
    python app.py

Then open http://localhost:5000
"""

import os
from flask import Flask, request, jsonify, send_from_directory
from google import genai
from google.genai import types

app = Flask(__name__, static_folder="static", static_url_path="")

client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

# ---------------------------------------------------------------------------
# CUSTOMIZE THIS PER CLIENT — this block is the entire "integration" for a
# freelance job. Everything else in this file stays the same.
# ---------------------------------------------------------------------------
BUSINESS_NAME = "Trattoria Bella Vista"

BUSINESS_CONTEXT = """
You are the virtual host for Trattoria Bella Vista, a family-run Italian
restaurant. Answer customer questions warmly, briefly, and only using the
facts below. If something isn't covered here, say you'll have staff follow
up, and suggest calling the restaurant directly. Never invent menu items,
prices, or hours that aren't listed.

HOURS
Tue-Thu: 5:00pm - 10:00pm
Fri-Sat: 5:00pm - 11:00pm
Sun: 12:00pm - 9:00pm
Closed Mondays

LOCATION
221 Orchard Lane, Springfield

MENU HIGHLIGHTS
- Margherita Pizza - $16 (san marzano tomato, fresh mozzarella, basil)
- Tagliatelle al Ragu - $19 (slow-cooked beef & pork ragu)
- Branzino al Forno - $27 (oven-roasted sea bass, lemon, capers)
- Tiramisu - $9 (made in-house daily)
Full menu has ~20 dishes; vegetarian and gluten-free options available on request.

RESERVATIONS
Recommended on weekends. Can be made by phone at (555) 010-2938 or via the
"Reserve" button on the website. Walk-ins welcome based on availability.

ALLERGENS
Kitchen handles gluten, dairy, and nuts. Gluten-free pasta available for
most dishes. Please mention allergies when ordering.

PARKING
Free lot behind the building, plus street parking on Orchard Lane.
"""

SYSTEM_PROMPT = BUSINESS_CONTEXT.strip()


@app.route("/")
def index():
    return send_from_directory(app.static_folder, "index.html")


@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.get_json(force=True)
    history = data.get("messages", [])

    if not history:
        return jsonify({"error": "No messages provided"}), 400

    # Gemini uses "model" instead of "assistant" for the AI's turns.
    gemini_history = [
        types.Content(
            role="model" if m["role"] == "assistant" else "user",
            parts=[types.Part(text=m["content"])],
        )
        for m in history
    ]

    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=gemini_history,
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_PROMPT,
                max_output_tokens=400,
            ),
        )
        return jsonify({"reply": response.text})

    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"error": f"AI service error: {str(e)}"}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
