from flask import Flask, request, jsonify
from flask_cors import CORS
from rag import build_index, search, load_csv_dataset
from pdf_loader import load_pdf
from fir_generator import generate_fir
from legal_analyzer import analyze_legal_text
from summarizer import summarize_text
from drafter import generate_draft
import requests
from openai import OpenAI
import os
from ocr import extract_text_from_pdf
from rag import search
import requests
from flask import request, jsonify


from openai import OpenAI

app = Flask(__name__)
CORS(app)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
client = OpenAI(api_key="your api key")

# Load dataset
# Load dataset 1 (your existing)
texts1 = load_csv_dataset(os.path.join("dataset", "Final_IC.csv"))

# Load dataset 2 (IPC dataset)
texts2 = load_csv_dataset(os.path.join("dataset", "ipc_sections.csv"))

# Combine both
all_texts = texts1 + texts2

# Build index on combined data
build_index(all_texts)
@app.route("/analyze-ai", methods=["POST"])
def analyze_ai():

    file = request.files["file"]
    path = "temp.pdf"
    file.save(path)

    text = load_pdf(path)

    prompt = f"""
You are an expert Indian legal document analyzer.

Analyze the following document:

{text}

Tasks:
1. Identify document type (Affidavit / Agreement / Deed / Lottery / Other)
2. Check if properly drafted
3. List missing clauses
4. Suggest improvements
5. Generate corrected version of document
6. Give a validity score (0–100)

Format response clearly.
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a professional Indian lawyer."},
            {"role": "user", "content": prompt}
        ]
    )

    answer = response.choices[0].message.content

    return jsonify({
        "analysis": answer,
        "preview": text[:500]
    })

@app.route("/")
def home():
    return "LexGuardian AI Backend Running"

@app.route("/ask", methods=["POST"])
@app.route("/ask", methods=["POST"])
def ask():
    try:
        data = request.get_json()

        query = data.get("query") or data.get("message")

        if not query:
            return jsonify({"error": "No query provided"}), 400

        results = search(query)

        answer = "\n".join([r["text"] for r in results]) if results else "No results found"

        return jsonify({ "answer": answer,
    "results": results})

    except Exception as e:
        return jsonify({"error": str(e)})
@app.route('/ask-pdf', methods=['POST'])
def ask_pdf():
    file = request.files['file']
    
    path = "uploads/" + file.filename
    file.save(path)

    text = extract_text_from_pdf(path)

    answer = search(text)   # your RAG function

    return {
        "extracted_text": text,
        "answer": answer
    }

@app.route("/analyze-document", methods=["POST"])
def analyze_document():

    file = request.files["file"]

    path = "temp_doc.pdf"
    file.save(path)

    # extract text
    text = load_pdf(path)

    # 🔍 detect type
    doc_type = detect_document_type(text)

    # 🧠 analyze
    analysis = analyze_document_content(text, doc_type)

    return jsonify({
        "type": doc_type,
        "analysis": analysis,
        "preview": text[:500]
    })
def detect_document_type(text):
    
    text = text.lower()

    if "affidavit" in text:
        return "Affidavit"

    elif "agreement" in text or "deed" in text:
        return "Legal Agreement / Deed"

    elif "lottery" in text:
        return "Lottery Document"

    else:
        return "Unknown Document"
def analyze_document_content(text, doc_type):
    
    missing = []
    suggestions = []

    # ✅ Affidavit check
    if doc_type == "Affidavit":

        if "name" not in text.lower():
            missing.append("Deponent Name")

        if "address" not in text.lower():
            missing.append("Address")

        if "declaration" not in text.lower():
            missing.append("Declaration Statement")

        if "signature" not in text.lower():
            missing.append("Signature")

        suggestions.append("Include notary attestation")
        suggestions.append("Add date and place")

    # ✅ Agreement / Deed check
    elif doc_type == "Legal Agreement / Deed":

        if "party" not in text.lower():
            missing.append("Parties involved")

        if "terms" not in text.lower():
            missing.append("Terms & Conditions")

        if "payment" not in text.lower():
            missing.append("Payment clause")

        if "termination" not in text.lower():
            missing.append("Termination clause")

        suggestions.append("Add dispute resolution clause")
        suggestions.append("Add jurisdiction clause")

    # ✅ Lottery check
    elif doc_type == "Lottery Document":

        if "ticket number" not in text.lower():
            missing.append("Ticket Number")

        if "date" not in text.lower():
            missing.append("Draw Date")

        suggestions.append("Verify authenticity with authority")

    return {
        "missing_clauses": missing,
        "suggestions": suggestions
    }

@app.route("/draft", methods=["POST"])
def draft():

    data = request.json
    prompt = data["prompt"]

    draft_text = generate_draft(prompt)

    return jsonify({"draft": draft_text})
    return jsonify({"answer": answer})
@app.route("/summarize", methods=["POST"])
def summarize():

    data = request.json
    text = data["text"]

    summary = summarize_text(text)

    return jsonify({"summary": summary})
@app.route("/generate-fir", methods=["POST"])
def fir():

    data = request.json
    description = data["description"]

    fir_text = generate_fir(description)

    return jsonify({"fir": fir_text})

@app.route("/upload", methods=["POST"])
def upload():

    file = request.files["file"]

    path = "temp.pdf"
    file.save(path)

    text = load_pdf(path)
    analysis = analyze_legal_text(text)

    return jsonify({
        "analysis": analysis,
        "text_preview": text[:500]
    })
@app.route('/nearby-police', methods=['POST'])
def nearby_police():
    data = request.get_json()

    lat = data.get("lat")
    lon = data.get("lon")

    if not lat or not lon:
        return jsonify({"error": "Location not provided"}), 400

    try:
        # OpenStreetMap Overpass API (NO API KEY)
        url = f"""
        https://overpass-api.de/api/interpreter?data=
        [out:json];
        node["amenity"="police"](around:5000,{lat},{lon});
        out;
        """

        response = requests.get(url)

        if response.status_code != 200:
            return jsonify({"error": "Failed to fetch data"}), 500

        data = response.json()

        results = []

        for el in data.get("elements", []):
            name = el.get("tags", {}).get("name", "Police Station")
            results.append({"name": name})

        return jsonify(results)

    except Exception as e:
        print(e)
        return jsonify({"error": "Server error"}), 500
if __name__ == "__main__":
    app.run(debug=True)