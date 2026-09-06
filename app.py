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
    export ANTHROPIC_API_KEY="your-key-here"
    python app.py

Then open http://localhost:5000
"""

import os
from flask import Flask, request, jsonify, send_from_directory
import anthropic

app = Flask(__name__, static_folder="static", static_url_path="")

client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

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

    try:
        response = client.messages.create(
            model="claude-haiku-4-5-20251001",  # fast + cheap, ideal for a support widget
            max_tokens=400,
            system=SYSTEM_PROMPT,
            messages=history,
        )
        reply_text = "".join(
            block.text for block in response.content if block.type == "text"
        )
        return jsonify({"reply": reply_text})

    except anthropic.APIError as e:
        return jsonify({"error": f"AI service error: {str(e)}"}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
