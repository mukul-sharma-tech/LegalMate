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
        "https://legal-mcci.vercel.app"  # Removed trailing slash
    ]
}})

# --- AI Handler Initialization ---
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Better error handling for initialization
if not GOOGLE_API_KEY:
    print("ERROR: GOOGLE_API_KEY environment variable not set!", file=sys.stderr)
    rag_handler = None
else:
    try:
        rag_handler = LegalRAG(api_key=GOOGLE_API_KEY)
        print("✓ LegalRAG handler initialized successfully")
    except Exception as e:
        print(f"FATAL: Could not initialize LegalRAG handler: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        rag_handler = None

# Health check endpoint
@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({
        "status": "healthy" if rag_handler else "degraded",
        "rag_initialized": rag_handler is not None
    }), 200

# --- API Endpoints ---

@app.route('/api/know-your-rights', methods=['POST'])
def know_your_rights():
    if not rag_handler:
        return jsonify({"error": "RAG system not initialized. Check server logs."}), 503
    
    data = request.get_json()
    if not data or 'query' not in data:
        return jsonify({"error": "Invalid request. 'query' field is required."}), 400
    
    try:
        result = rag_handler.get_rights(data['query'])
        return jsonify(result.dict())
    except Exception as e:
        print(f"Error in know_your_rights: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return jsonify({"error": f"Failed to process query: {str(e)}"}), 500

@app.route('/api/simplify', methods=['POST'])
def simplify_document():
    if not rag_handler:
        return jsonify({"error": "RAG system not initialized. Check server logs."}), 503
    
    data = request.get_json()
    if not data or 'text' not in data:
        return jsonify({"error": "Invalid request. 'text' field is required."}), 400
    
    try:
        result = rag_handler.simplify_document(data['text'])
        return jsonify(result.dict())
    except Exception as e:
        print(f"Error in simplify_document: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return jsonify({"error": f"Failed to simplify document: {str(e)}"}), 500

@app.route("/api/advise", methods=["POST"])
def advise_case():
    if not rag_handler:
        return jsonify({"error": "RAG system not initialized. Check server logs."}), 503
    
    data = request.get_json()
    if not data or 'case_text' not in data:
        return jsonify({"error": "Invalid request. 'case_text' field is required."}), 400
    
    try:
        result = rag_handler.advise_on_case(data['case_text'])
        return jsonify(result.dict())
    except Exception as e:
        print(f"Error in advise_case: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return jsonify({"error": f"Failed to analyze case: {str(e)}"}), 500

@app.route("/api/ask-vakil", methods=["POST"])
def ask_vakil():
    if not rag_handler:
        return jsonify({"error": "RAG system not initialized. Check server logs."}), 503
    
    data = request.get_json()
    if not data or 'document_text' not in data or 'question' not in data:
        return jsonify({"error": "Invalid request. 'document_text' and 'question' fields are required."}), 400
    
    try:
        result = rag_handler.ask_question_about_document(
            data['document_text'], 
            data['question']
        )
        return jsonify({"answer": result})
    except Exception as e:
        print(f"Error in ask_vakil: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return jsonify({"error": f"Failed to get answer: {str(e)}"}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    # IMPORTANT: Set debug=False in production
    app.run(host='0.0.0.0', port=port, debug=False)
