# AI Chat Widget Demo — Trattoria Bella Vista

A working example of the exact thing to pitch small businesses: an AI chat
widget on their website that answers customer questions using only their
own info (hours, menu, policies) — no hallucinated details.

## Run it locally

```bash
cd ai-chat-demo
pip install -r requirements.txt
export ANTHROPIC_API_KEY="your-key-here"   # get one at console.anthropic.com
python app.py
```

Open http://localhost:5000 and click "Ask us anything" in the bottom right.

## How it works

- `static/index.html` + `style.css` + `script.js` — the restaurant's page and
  the chat widget UI. Plain HTML/CSS/JS, no build step.
- `app.py` — a small Flask server. `/api/chat` takes the conversation so far
  and asks the Claude API to reply, using `BUSINESS_CONTEXT` as its only
  source of facts about the business.

## Turning this into a real client project

1. Replace `BUSINESS_NAME` and `BUSINESS_CONTEXT` in `app.py` with the real
   client's hours, menu/services, policies, and contact info. That's the
   entire integration — nothing else needs to change.
2. Swap the color palette and fonts in `style.css` to match their branding.
3. Deploy (Render, Railway, and Fly.io all have free/cheap tiers that work
   well for this). Point their existing site's DNS or embed the widget via
   an `<iframe>` or a small `<script>` snippet if they don't want to move
   hosting.
4. Charge a flat setup fee ($150–400 depending on how much content needs
   organizing) plus a small monthly fee ($20–50) to cover hosting + API
   costs and ongoing tweaks.

## Notes on cost

`claude-haiku-4-5-20251001` is used because it's fast and inexpensive —
well suited to short, high-volume customer questions. For a business with
heavier or more technical support needs, swapping in a stronger model in
`app.py` is a one-line change.
