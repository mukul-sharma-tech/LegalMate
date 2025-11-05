import os
import sys
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

# --- Local Imports ---
from rag_legal import LegalRAG

# Load environment variables
load_dotenv()

# --- App Initialization ---
app = Flask(__name__)
CORS(app, resources={r"/api/*": {
    "origins": [
        "http://localhost:3000",
        "https://legal-mate-ai.vercel.app",
        "https://legal-mcci.vercel.app" # Cleaned up URL
    ]
}})

# --- AI Handler Initialization ---
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
rag_handler = None

if not GOOGLE_API_KEY:
    print("FATAL ERROR: GOOGLE_API_KEY environment variable is not set.", file=sys.stderr)
else:
    try:
        rag_handler = LegalRAG(api_key=GOOGLE_API_KEY)
        print("--- LegalRAG handler initialized successfully ---")
    except Exception as e:
        print(f"FATAL ERROR: Could not initialize LegalRAG handler: {e}", file=sys.stderr)


# --- API Endpoints ---

@app.route('/api/know-your-rights', methods=['POST'])
def know_your_rights():
    if not rag_handler:
        return jsonify({"error": "Server error: RAG system not initialized"}), 503
        
    data = request.get_json()
    if not data or 'query' not in data:
        return jsonify({"error": "Invalid request: 'query' field missing"}), 400
        
    try:
        result = rag_handler.get_rights(data['query'])
        # --- FIX: Use .model_dump() for Pydantic v2 ---
        return jsonify(result.model_dump())
    except Exception as e:
        print(f"Error in know_your_rights: {e}", file=sys.stderr)
        return jsonify({"error": "Failed to process query"}), 500

@app.route('/api/simplify', methods=['POST'])
def simplify_document():
    if not rag_handler:
        return jsonify({"error": "Server error: RAG system not initialized"}), 503
        
    data = request.get_json()
    if not data or 'text' not in data:
        return jsonify({"error": "Invalid request: 'text' field missing"}), 400
        
    try:
        result = rag_handler.simplify_document(data['text'])
        # --- FIX: Use .model_dump() for Pydantic v2 ---
        return jsonify(result.model_dump())
    except Exception as e:
        print(f"Error in simplify_document: {e}", file=sys.stderr)
        return jsonify({"error": "Failed to simplify document"}), 500

@app.route("/api/advise", methods=["POST"])
def advise_case():
    if not rag_handler:
        return jsonify({"error": "Server error: RAG system not initialized"}), 503
        
    data = request.get_json()
    if not data or 'case_text' not in data:
        return jsonify({"error": "Invalid request: 'case_text' field missing"}), 400
        
    try:
        result = rag_handler.advise_on_case(data['case_text'])
        # --- FIX: Use .model_dump() for Pydantic v2 ---
        return jsonify(result.model_dump())
    except Exception as e:
        print(f"Error in advise_case: {e}", file=sys.stderr)
        return jsonify({"error": "Failed to analyze case"}), 500

@app.route("/api/ask-vakil", methods=["POST"])
def ask_vakil():
    if not rag_handler:
        return jsonify({"error": "Server error: RAG system not initialized"}), 503
        
    data = request.get_json()
    if not data or 'document_text' not in data or 'question' not in data:
        return jsonify({"error": "Invalid request: missing 'document_text' or 'question'"}), 400
        
    try:
        result = rag_handler.ask_question_about_document(
            data['document_text'], 
            data['question']
        )
        return jsonify({"answer": result})
    except Exception as e:
        print(f"Error in ask_vakil: {e}", file=sys.stderr)
        return jsonify({"error": "Failed to get answer"}), 500

# Health check route for Render
@app.route("/health")
def health_check():
    return jsonify({"status": "healthy"}), 200

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    # debug=False is important for production/gunicorn
    app.run(host='0.0.0.0', port=port, debug=False)
