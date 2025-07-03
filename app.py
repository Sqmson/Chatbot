from flask import Flask, render_template, request, jsonify
import requests, os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()
API_KEY = os.getenv("API_KEY")

app = Flask(__name__)

# === FAQ data ===
FAQ = [
    {"q": "What is NITA-U?", "a": "The National Information Technology Authority Uganda (NITA-U) is an autonomous statutory body established under the NITA-U Act 2009 to coordinate, promote, and regulate ICT across the public and private sectors in Uganda."},
    {"q": "When was NITA-U established?", "a": "NITA-U was established by an Act of Parliament in 2009, and began operations around 2010."},
    {"q": "Where is NITA-U headquartered?", "a": "Its headquarters are on Lugogo Rotary Avenue in Kampala."},
    {"q": "What is the National Backbone Infrastructure (NBI)?", "a": "The NBI is a nationwide government‑owned fiber‑optic network managed by NITA-U to connect government institutions."},
    {"q": "What services does NITA-U provide?", "a": "They provide broadband (NBI), cloud (G‑Cloud), data centre services, cybersecurity (CERT‑UG), e‑Government platforms like UGhub, UMCS, UgPass, and training."},
    {"q": "What is CERT‑UG?", "a": "The Uganda National Computer Emergency Response Team, run by NITA‑U, manages cybersecurity incidents and awareness."},
    {"q": "Who is the Executive Director of NITA-U?", "a": "Dr. Hatwib Mugasa is the current Executive Director."},
    {"q": "What is UGPass?", "a": "UGPass is a national digital authentication platform that won the World Summit on the Information Society (WSIS) award in 2024."},
    {"q": "How can agencies connect to NBI?", "a": "Government agencies can apply formally; NITA‑U conducts site assessment and provisions leased lines or dark fibre."},
    {"q": "Does NITA‑U regulate ICT procurement?", "a": "Yes, NITA‑U enforces technical ICT standards and compliance in public sector procurement."},
    {"q": "What is GovNet?", "a": "GovNet is a secure private network connecting government institutions across Uganda."},
    {"q": "Does NITA‑U offer training?", "a": "Yes, NITA‑U provides ICT capacity building to public servants and partners."},
    {"q": "How do I contact NITA‑U?", "a": "Via their website, email info@nita.go.ug, phone +256 417 801038, or visit their office at Palm Courts, Kampala."},
    {"q": "What awards has NITA‑U won?", "a": "In 2024, UGPass and their service design won global WSIS awards."},
    {"q": "What is UGhub?", "a": "UGhub is a government systems integration platform allowing secure data sharing across ministries."}
]

# === Prompt Engineering ===
system_prompt = "You are a helpful AI assistant for the National Information Technology Authority Uganda (NITA-U).\n"
system_prompt += "Use the following institutional information and FAQs to answer questions clearly:\n\n"
for item in FAQ:
    system_prompt += f"Q: {item['q']}\nA: {item['a']}\n\n"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    user_message = request.json.get("message", "").strip().lower()

    # Normal request to NVIDIA AI model
    invoke_url = "https://integrate.api.nvidia.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Accept": "application/json"
    }

    payload = {
        "model": "google/gemma-3n-e4b-it",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message}
        ],
        "max_tokens": 512,
        "temperature": 1.9,
        "top_p": 0.9,
        "stream": False
    }

    response = requests.post(invoke_url, headers=headers, json=payload)
    data = response.json()
    reply = data["choices"][0]["message"]["content"]
    return jsonify({"reply": reply})

@app.route("/initial", methods=["GET"])
def initial():
    hour = datetime.now().hour
    if hour < 12:
        time_greeting = "Good morning"
    elif 12 <= hour < 17:
        time_greeting = "Good afternoon"
    else:
        time_greeting = "Good evening"

    intro = (
        f"{time_greeting}! Here to ease your search."
        "\n\nJust ask away or perhaps you'd like to take a wild venture."
    )
    suggestions = [
        
    ]
    return jsonify({"reply": intro, "suggestions": suggestions})

if __name__ == "__main__":
    app.run(debug=True)
