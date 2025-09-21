# import os
# from flask import Flask, request, jsonify
# from flask_cors import CORS
# from dotenv import load_dotenv

# # --- Langchain & Gemini Imports ---
# import google.generativeai as genai
# from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
# from langchain.vectorstores import FAISS
# from langchain.text_splitter import RecursiveCharacterTextSplitter
# from langchain.chains import create_retrieval_chain
# from langchain.chains.combine_documents import create_stuff_documents_chain
# from langchain_core.prompts import ChatPromptTemplate
# from langchain_core.pydantic_v1 import BaseModel, Field
# from langchain_core.output_parsers import JsonOutputParser


# # --- Load Environment Variables ---
# load_dotenv()
# GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
# if not GOOGLE_API_KEY:
#     raise ValueError("GOOGLE_API_KEY not found in environment variables.")

# genai.configure(api_key=GOOGLE_API_KEY)


# # --- Initialize Flask App ---
# app = Flask(__name__)
# CORS(app) # Enable Cross-Origin Resource Sharing

# # --- Global RAG Chain Variable ---
# rag_chain = None

# # --- Pydantic Output Schemas for JSON parsing ---
# class SimplifiedPoints(BaseModel):
#     """A list of simplified points from a legal document."""
#     points: list[dict] = Field(description="A list of JSON objects, each with a 'title' and 'text' key.")

# class CaseAnalysis(BaseModel):
#     """A structured analysis of a user's legal case."""
#     analysis: list[dict] = Field(description="A list of JSON objects, each with a 'type', 'title', and 'text' key.")

# class RightsInfo(BaseModel):
#     """Structured information about a user's legal rights."""
#     explanation: str = Field(description="A simple, plain-language explanation of the user's rights in this context.")
#     relevantLaws: list[dict] = Field(description="A list of relevant laws, each with a 'title' and 'text'.")
#     guidance: str = Field(description="Actionable guidance or next steps for the user.")
#     disclaimer: str = Field(description="A standard disclaimer that this is not legal advice.")


# # --- RAG Pipeline Setup Function ---
# def setup_rag_chain():
#     """
#     Initializes the RAG chain by loading documents, creating embeddings,
#     and setting up the retrieval and generation components.
#     """
#     global rag_chain
#     try:
#         # 1. Initialize Model & Embeddings
#         llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash-preview-05-20", temperature=0.3)
#         embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

#         # 2. Load and Split Documents
#         # For a real app, you would load many documents. Here, we use one for the demo.
#         with open("knowledge_base/payment_of_wages_act.txt", "r") as f:
#             knowledge_text = f.read()
        
#         text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
#         documents = text_splitter.create_documents([knowledge_text])
        
#         # 3. Create Vector Store (FAISS)
#         vector_store = FAISS.from_documents(documents, embeddings)
#         retriever = vector_store.as_retriever()

#         # 4. Create Prompt Template
#         system_prompt = (
#             "You are an expert legal assistant. Your task is to answer a user's question about their rights "
#             "based *only* on the provided legal context. Do not use any outside knowledge. "
#             "Your response must be structured as a JSON object that strictly follows the provided schema. "
#             "Provide clear, simple explanations and actionable guidance. "
#             "Context: {context}"
#         )
#         prompt = ChatPromptTemplate.from_messages([("system", system_prompt), ("human", "{input}")])
        
#         # 5. Create Chains
#         question_answer_chain = create_stuff_documents_chain(llm, prompt)
#         rag_chain = create_retrieval_chain(retriever, question_answer_chain)
        
#         print("✅ RAG Chain setup complete.")

#     except Exception as e:
#         print(f"❌ Error setting up RAG chain: {e}")


# # --- API Endpoints ---

# @app.route('/api/simplify', methods=['POST'])
# def simplify_document():
#     """Directly calls Gemini API to simplify a legal document."""
#     try:
#         data = request.get_json()
#         if not data or 'text' not in data:
#             return jsonify({"error": "No text provided"}), 400

#         legal_text = data['text']
        
#         parser = JsonOutputParser(pydantic_object=SimplifiedPoints)
#         prompt = ChatPromptTemplate.from_messages([
#             ("system", "You are an expert legal assistant. Simplify the following legal text into a series of key points. Your response must be a JSON object that follows this schema: {format_instructions}"),
#             ("human", "{text}")
#         ])
        
#         model = ChatGoogleGenerativeAI(model="gemini-2.5-flash-preview-05-20", temperature=0.1)
#         chain = prompt | model | parser
        
#         result = chain.invoke({
#             "text": legal_text,
#             "format_instructions": parser.get_format_instructions()
#         })
        
#         return jsonify(result['points'])

#     except Exception as e:
#         print(f"Error in /api/simplify: {e}")
#         return jsonify({"error": "Failed to process the document"}), 500


# @app.route('/api/advise', methods=['POST'])
# def get_legal_advice():
#     """Directly calls Gemini API to analyze a user's case."""
#     try:
#         data = request.get_json()
#         if not data or 'caseText' not in data:
#             return jsonify({"error": "No case text provided"}), 400

#         case_text = data['caseText']
        
#         parser = JsonOutputParser(pydantic_object=CaseAnalysis)
#         prompt = ChatPromptTemplate.from_messages([
#             ("system", "You are an AI legal advisor. Analyze the user's situation and identify key legal points and a final recommendation. Your response must be a JSON object that follows this schema: {format_instructions}"),
#             ("human", "{case}")
#         ])
        
#         model = ChatGoogleGenerativeAI(model="gemini-2.5-flash-preview-05-20", temperature=0.5)
#         chain = prompt | model | parser
        
#         result = chain.invoke({
#             "case": case_text,
#             "format_instructions": parser.get_format_instructions()
#         })
        
#         return jsonify(result['analysis'])

#     except Exception as e:
#         print(f"Error in /api/advise: {e}")
#         return jsonify({"error": "Failed to analyze the case"}), 500


# @app.route('/api/know-your-rights', methods=['POST'])
# def know_your_rights():
#     """Uses the RAG chain to answer a user's question."""
#     if rag_chain is None:
#         return jsonify({"error": "RAG chain is not initialized"}), 500
        
#     try:
#         data = request.get_json()
#         if not data or 'query' not in data:
#             return jsonify({"error": "No query provided"}), 400

#         user_query = data['query']
        
#         # We need to add a parser to the end of our RAG chain
#         parser = JsonOutputParser(pydantic_object=RightsInfo)
        
#         # The rag_chain gives us 'context' and 'answer'. We want to parse the 'answer'.
#         # This is a slightly more advanced LangChain Expression Language (LCEL) usage.
#         runnable_with_parser = rag_chain | (lambda output: output['answer']) | parser
        
#         result = runnable_with_parser.invoke({"input": user_query})
        
#         return jsonify(result)

#     except Exception as e:
#         print(f"Error in /api/know-your-rights: {e}")
#         return jsonify({"error": "Failed to get rights information"}), 500


# if __name__ == '__main__':
#     setup_rag_chain()
#     app.run(host='0.0.0.0', port=5000, debug=True)

# import os
# from flask import Flask, request, jsonify
# from flask_cors import CORS
# from dotenv import load_dotenv

# # --- LangChain & Google Generative AI Imports ---
# from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
# from langchain.prompts import ChatPromptTemplate
# from langchain_community.document_loaders import TextLoader
# from langchain.text_splitter import RecursiveCharacterTextSplitter
# from langchain_community.vectorstores import FAISS
# from langchain.chains.combine_documents import create_stuff_documents_chain
# from langchain.chains import create_retrieval_chain, create_extraction_chain
# from langchain.output_parsers.openai_functions import JsonOutputFunctionsParser

# # Load environment variables
# load_dotenv()

# # --- App Initialization ---
# app = Flask(__name__)
# CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000"}})

# # --- AI Model Initialization ---
# llm = ChatGoogleGenerativeAI(
#     model="gemini-2.5-flash-preview-05-20",
#     temperature=0.3,
#     google_api_key=os.getenv("GOOGLE_API_KEY")
# )

# # --- Caching for RAG Pipeline ---
# rag_chain_cache = {}

# # --- Schemas for structured output ---
# simplify_schema = {
#     "name": "document_simplifier",
#     "description": "Formats a simplified summary of a legal document.",
#     "parameters": {
#         "type": "object",
#         "properties": {
#             "summary_points": {
#                 "type": "array",
#                 "description": "A list of simplified points from the document.",
#                 "items": {
#                     "type": "object",
#                     "properties": {
#                         "title": {"type": "string"},
#                         "text": {"type": "string"}
#                     },
#                     "required": ["title", "text"]
#                 }
#             }
#         },
#         "required": ["summary_points"]
#     }
# }

# advisor_schema = {
#     "name": "legal_advisor",
#     "description": "Formats a legal analysis of a user's personal case.",
#     "parameters": {
#         "type": "object",
#         "properties": {
#             "analysis_points": {
#                 "type": "array",
#                 "description": "A list of analysis points for the user's case.",
#                 "items": {
#                     "type": "object",
#                     "properties": {
#                         "type": {"type": "string", "enum": ["point", "recommendation"]},
#                         "title": {"type": "string"},
#                         "text": {"type": "string"}
#                     },
#                     "required": ["type", "title", "text"]
#                 }
#             }
#         },
#         "required": ["analysis_points"]
#     }
# }

# rights_schema = {
#     "name": "know_your_rights_formatter",
#     "description": "Formats the answer to a user's rights-based question.",
#     "parameters": {
#         "type": "object",
#         "properties": {
#             "explanation": {"type": "string"},
#             "relevantLaws": {
#                 "type": "array",
#                 "items": {
#                     "type": "object",
#                     "properties": {
#                         "title": {"type": "string"},
#                         "text": {"type": "string"}
#                     },
#                     "required": ["title", "text"]
#                 }
#             },
#             "guidance": {"type": "string"},
#             "disclaimer": {"type": "string"}
#         },
#         "required": ["explanation", "relevantLaws", "guidance", "disclaimer"]
#     }
# }

# # --- API Endpoints ---

# @app.route('/api/simplify', methods=['POST'])
# def simplify_document():
#     data = request.get_json()
#     if not data or 'text' not in data:
#         return jsonify({"error": "No text provided"}), 400

#     prompt = ChatPromptTemplate.from_messages([
#         ("system", "You are an expert legal assistant. Simplify the text into points with title & explanation."),
#         ("human", "{legal_text}")
#     ])

#     parser = JsonOutputFunctionsParser(key_name="summary_points")
#     chain = create_extraction_chain(
#         llm=llm,
#         prompt=prompt,
#         structured_output_parser=parser
#     )

#     response = chain.invoke({"legal_text": data['text']})
#     return jsonify(response)


# @app.route('/api/advise', methods=['POST'])
# def advise_case():
#     data = request.get_json()
#     if not data or 'case_text' not in data:
#         return jsonify({"error": "No case text provided"}), 400

#     prompt = ChatPromptTemplate.from_messages([
#         ("system", "You are an AI Legal Advisor. Identify legal points and recommendations."),
#         ("human", "{user_case}")
#     ])

#     parser = JsonOutputFunctionsParser(key_name="analysis_points")
#     chain = create_extraction_chain(
#         llm=llm,
#         prompt=prompt,
#         structured_output_parser=parser
#     )

#     response = chain.invoke({"user_case": data['case_text']})
#     return jsonify(response)


# def get_rag_chain():
#     """Initializes and caches the RAG chain."""
#     if "rag_chain" in rag_chain_cache:
#         return rag_chain_cache["rag_chain"]

#     # Embeddings
#     embeddings = GoogleGenerativeAIEmbeddings(
#         model="models/embedding-001",
#         google_api_key=os.getenv("GOOGLE_API_KEY")
#     )

#     # Load documents
#     kb_path = "./knowledge_base/payment_of_wages_act.txt"
#     if not os.path.exists(kb_path):
#         raise FileNotFoundError(f"{kb_path} not found. Please add the file.")

#     loader = TextLoader(kb_path)
#     docs = loader.load()
#     splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
#     split_docs = splitter.split_documents(docs)

#     # Vector store
#     vector_store = FAISS.from_documents(split_docs, embeddings)
#     retriever = vector_store.as_retriever()

#     # Prompt
#     system_prompt = (
#         "You are an expert legal assistant. Answer user's questions based only on provided context.\n\n"
#         "Context: {context}"
#     )
#     prompt = ChatPromptTemplate.from_messages([
#         ("system", system_prompt),
#         ("human", "{input}")
#     ])

#     question_answer_chain = create_stuff_documents_chain(llm, prompt)
#     rag_chain = create_retrieval_chain(retriever, question_answer_chain)
#     rag_chain_cache["rag_chain"] = rag_chain
#     return rag_chain


# @app.route('/api/know-your-rights', methods=['POST'])
# def know_your_rights():
#     data = request.get_json()
#     if not data or 'query' not in data:
#         return jsonify({"error": "No query provided"}), 400

#     rag_chain = get_rag_chain()
#     response = rag_chain.invoke({"input": data['query']})
#     raw_answer = response['answer']

#     formatting_prompt = ChatPromptTemplate.from_messages([
#         ("system", "You are an expert at re-formatting text into structured JSON."),
#         ("human", "Format the following info for user's question: '{question}'\n\nInfo:\n{information}")
#     ])

#     parser = JsonOutputFunctionsParser()
#     formatting_chain = create_extraction_chain(
#         llm=llm,
#         prompt=formatting_prompt,
#         structured_output_parser=parser
#     )

#     structured_response = formatting_chain.invoke({
#         "question": data['query'],
#         "information": raw_answer
#     })

#     return jsonify(structured_response)


# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=5000, debug=True)

# import os
# from flask import Flask, request, jsonify
# from flask_cors import CORS
# from dotenv import load_dotenv

# # --- LangChain & Google Generative AI Imports ---
# from langchain_google_genai import ChatGoogleGenerativeAI
# from langchain.prompts import ChatPromptTemplate
# from langchain_community.document_loaders import TextLoader
# from langchain.text_splitter import RecursiveCharacterTextSplitter
# from langchain_community.vectorstores import FAISS
# from langchain.chains import RetrievalQA

# # Load environment variables
# load_dotenv()

# # --- App Initialization ---
# app = Flask(__name__)
# CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000"}})

# # --- LLM Initialization ---
# llm = ChatGoogleGenerativeAI(
#     model="gemini-2.5-flash-preview-05-20",
#     temperature=0.3,
#     google_api_key=os.getenv("GOOGLE_API_KEY")
# )

# # --- RAG Chain Cache ---
# rag_chain_cache = {}

# def get_rag_chain():
#     """Initialize and cache RAG chain for legal documents."""
#     if "rag_chain" in rag_chain_cache:
#         return rag_chain_cache["rag_chain"]

#     # Embeddings
#     embeddings = GoogleGenerativeAIEmbeddings(
#         model="models/embedding-001",
#         google_api_key=os.getenv("GOOGLE_API_KEY")
#     )

#     # Load legal document
#     kb_path = "./knowledge_base/payment_of_wages_act.txt"
#     if not os.path.exists(kb_path):
#         raise FileNotFoundError(f"{kb_path} not found!")

#     loader = TextLoader(kb_path)
#     docs = loader.load()

#     # Split into chunks
#     splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
#     split_docs = splitter.split_documents(docs)

#     # Vector store
#     vector_store = FAISS.from_documents(split_docs, embeddings)
#     retriever = vector_store.as_retriever()

#     # Create RetrievalQA chain
#     rag_chain = RetrievalQA.from_chain_type(
#         llm=llm,
#         chain_type="stuff",
#         retriever=retriever,
#         return_source_documents=True
#     )
#     rag_chain_cache["rag_chain"] = rag_chain
#     return rag_chain

# # --- API Endpoints ---

# @app.route('/api/know-your-rights', methods=['POST'])
# def know_your_rights():
#     data = request.get_json()
#     if not data or 'query' not in data:
#         return jsonify({"error": "No query provided"}), 400

#     rag_chain = get_rag_chain()
#     result = rag_chain.run(data['query'])
#     return jsonify({"answer": result})

# @app.route('/api/simplify', methods=['POST'])
# def simplify_document():
#     data = request.get_json()
#     if not data or 'text' not in data:
#         return jsonify({"error": "No text provided"}), 400

#     prompt_text = (
#         "You are an expert legal assistant. "
#         "Simplify the following legal text into JSON with key 'summary_points', "
#         "where 'summary_points' is a list of objects with 'title' and 'text'.\n\n"
#         f"Legal Text:\n{data['text']}"
#     )

#     try:
#         # Call the LLM
#         response = llm.invoke([{"role": "user", "content": prompt_text}])
#         content = response.content if hasattr(response, "content") else str(response)

#         # DEBUG: log raw response
#         print("Raw LLM response:", content)

#         # Attempt JSON parsing
#         import json
#         try:
#             parsed = json.loads(content)
#         except json.JSONDecodeError:
#             # Try to extract JSON manually from the text
#             import re
#             match = re.search(r'(\{.*\})', content, re.DOTALL)
#             if match:
#                 parsed = json.loads(match.group(1))
#             else:
#                 raise ValueError("Could not parse JSON from LLM response")

#         if "summary_points" not in parsed or not isinstance(parsed["summary_points"], list):
#             raise ValueError("Missing 'summary_points' key or invalid format")

#         return jsonify(parsed)

#     except Exception as e:
#         # Return full error info to debug
#         return jsonify({
#             "error": "Failed to simplify document",
#             "exception": str(e),
#             "raw_response": content
#         }), 500
        
# @app.route("/api/advise", methods=["POST"])
# def advise_case():
#     data = request.get_json()
#     case_text = data.get("case_text", "").strip()
#     if not case_text:
#         return jsonify({"error": "No case text provided"}), 400

#     system_text = "You are a legal AI assistant. Respond ONLY in JSON with analysis_points."

#     messages = [
#         {"role": "system", "content": system_text},
#         {"role": "user", "content": case_text}
#     ]

#     try:
#         response = llm.invoke(messages)
#         content = getattr(response, "content", str(response))
#         analysis_points = json.loads(content).get("analysis_points", [])
#         return jsonify({"analysis_points": analysis_points})
#     except Exception as e:
#         return jsonify({"error": str(e), "raw_response": content}), 500

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=5000, debug=True)



# import os
# import json
# import re
# from flask import Flask, request, jsonify
# from flask_cors import CORS
# from dotenv import load_dotenv

# # --- LangChain & Google Generative AI Imports ---
# from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
# from langchain.prompts import ChatPromptTemplate
# from langchain_community.document_loaders import TextLoader
# from langchain.text_splitter import RecursiveCharacterTextSplitter
# from langchain_community.vectorstores import FAISS
# from langchain.chains import RetrievalQA

# # Load environment variables
# load_dotenv()

# # --- App Initialization ---
# app = Flask(__name__)
# CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000"}})

# # --- LLM Initialization ---
# llm = ChatGoogleGenerativeAI(
#     model="gemini-2.5-flash-preview-05-20",
#     temperature=0.3,
#     google_api_key=os.getenv("GOOGLE_API_KEY")
# )

# # --- RAG Chain Cache ---
# rag_chain_cache = {}

# def get_rag_chain():
#     """Initialize and cache RAG chain for legal documents."""
#     if "rag_chain" in rag_chain_cache:
#         return rag_chain_cache["rag_chain"]

#     # Embeddings
#     embeddings = GoogleGenerativeAIEmbeddings(
#         model="models/embedding-001",
#         google_api_key=os.getenv("GOOGLE_API_KEY")
#     )

#     # Load legal document
#     kb_path = "./knowledge_base/payment_of_wages_act.txt"
#     if not os.path.exists(kb_path):
#         raise FileNotFoundError(f"{kb_path} not found!")

#     loader = TextLoader(kb_path)
#     docs = loader.load()

#     # Split into chunks
#     splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
#     split_docs = splitter.split_documents(docs)

#     # Vector store
#     vector_store = FAISS.from_documents(split_docs, embeddings)
#     retriever = vector_store.as_retriever()

#     # Create RetrievalQA chain
#     rag_chain = RetrievalQA.from_chain_type(
#         llm=llm,
#         chain_type="stuff",
#         retriever=retriever,
#         return_source_documents=True
#     )
#     rag_chain_cache["rag_chain"] = rag_chain
#     return rag_chain

# def parse_json_from_response(content):
#     """Helper function to extract JSON from LLM response."""
#     try:
#         # First try direct parsing
#         return json.loads(content)
#     except json.JSONDecodeError:
#         # Try to extract JSON from markdown code blocks
#         json_match = re.search(r'```json\s*(.*?)\s*```', content, re.DOTALL)
#         if json_match:
#             try:
#                 return json.loads(json_match.group(1))
#             except json.JSONDecodeError:
#                 pass
        
#         # Try to find any JSON object in the text
#         json_match = re.search(r'(\{.*\})', content, re.DOTALL)
#         if json_match:
#             try:
#                 return json.loads(json_match.group(1))
#             except json.JSONDecodeError:
#                 pass
        
#         raise ValueError("Could not parse JSON from LLM response")

# # --- API Endpoints ---

# @app.route('/api/know-your-rights', methods=['POST'])
# def know_your_rights():
#     data = request.get_json()
#     if not data or 'query' not in data:
#         return jsonify({"error": "No query provided"}), 400

#     try:
#         # Temporary workaround: Use general legal knowledge instead of RAG
#         # due to Google embedding API quota limits
#         formatting_prompt = f"""
#         You are a legal expert with knowledge of employment law, particularly the Payment of Wages Act. 
#         Answer the user's question about their legal rights and format your response into this exact JSON structure:
        
#         {{
#             "explanation": "A simple, plain-language explanation of the user's rights based on general legal principles",
#             "relevantLaws": [
#                 {{
#                     "title": "The title of the relevant law or legal principle",
#                     "text": "A simple explanation of what the law means"
#                 }}
#             ],
#             "guidance": "Actionable guidance or next steps for the user",
#             "disclaimer": "This is for informational purposes only and does not constitute legal advice. Please consult with a qualified attorney for personalized legal advice."
#         }}
        
#         User's question: {data['query']}
        
#         Focus on employment rights, wage payment laws, and worker protections. Provide practical, actionable advice.
#         Respond with ONLY the JSON, no additional text:
#         """
        
#         response = llm.invoke([{"role": "user", "content": formatting_prompt}])
#         content = response.content if hasattr(response, "content") else str(response)
        
#         parsed_response = parse_json_from_response(content)
#         return jsonify(parsed_response)
        
#     except Exception as e:
#         print(f"Error in know_your_rights: {str(e)}")
#         return jsonify({"error": f"Failed to process rights query: {str(e)}"}), 500

# @app.route('/api/simplify', methods=['POST'])
# def simplify_document():
#     data = request.get_json()
#     if not data or 'text' not in data:
#         return jsonify({"error": "No text provided"}), 400

#     prompt_text = f"""
#     You are an expert legal assistant. Simplify the following legal text into a JSON response with this exact structure:
    
#     {{
#         "summary_points": [
#             {{
#                 "title": "A short, clear title for the point",
#                 "text": "The simplified explanation of the point"
#             }}
#         ]
#     }}
    
#     Legal Text to simplify:
#     {data['text']}
    
#     Respond with ONLY the JSON, no additional text:
#     """

#     try:
#         response = llm.invoke([{"role": "user", "content": prompt_text}])
#         content = response.content if hasattr(response, "content") else str(response)
        
#         print("Raw LLM response:", content)  # Debug log
        
#         parsed_response = parse_json_from_response(content)
        
#         # Validate the response structure
#         if "summary_points" not in parsed_response or not isinstance(parsed_response["summary_points"], list):
#             raise ValueError("Missing 'summary_points' key or invalid format")

#         return jsonify(parsed_response)

#     except Exception as e:
#         print(f"Error in simplify_document: {str(e)}")
#         return jsonify({
#             "error": "Failed to simplify document",
#             "details": str(e)
#         }), 500
        
# @app.route("/api/advise", methods=["POST"])
# def advise_case():
#     data = request.get_json()
#     if not data or 'case_text' not in data:
#         return jsonify({"error": "No case text provided"}), 400
    
#     case_text = data.get("case_text", "").strip()
#     if not case_text:
#         return jsonify({"error": "Case text is empty"}), 400

#     prompt_text = f"""
#     You are an AI Legal Advisor. Analyze the user's situation and provide a JSON response with this exact structure:
    
#     {{
#         "analysis_points": [
#             {{
#                 "type": "point",
#                 "title": "A short, clear title for the legal point",
#                 "text": "The detailed explanation of the legal point"
#             }},
#             {{
#                 "type": "recommendation", 
#                 "title": "A short, clear title for the recommendation",
#                 "text": "The detailed explanation of the recommendation"
#             }}
#         ]
#     }}
    
#     Each item must have "type" as either "point" (for legal analysis) or "recommendation" (for actionable advice).
#     Provide multiple points and recommendations as relevant.
    
#     User's case:
#     {case_text}
    
#     Respond with ONLY the JSON, no additional text:
#     """

#     try:
#         response = llm.invoke([{"role": "user", "content": prompt_text}])
#         content = response.content if hasattr(response, "content") else str(response)
        
#         print("Raw LLM response:", content)  # Debug log
        
#         parsed_response = parse_json_from_response(content)
        
#         # Validate the response structure
#         if "analysis_points" not in parsed_response or not isinstance(parsed_response["analysis_points"], list):
#             raise ValueError("Missing 'analysis_points' key or invalid format")
        
#         # Validate each analysis point
#         for point in parsed_response["analysis_points"]:
#             if not all(key in point for key in ["type", "title", "text"]):
#                 raise ValueError("Invalid analysis point structure")
#             if point["type"] not in ["point", "recommendation"]:
#                 raise ValueError("Invalid analysis point type")

#         return jsonify(parsed_response)
        
#     except Exception as e:
#         print(f"Error in advise_case: {str(e)}")
#         return jsonify({
#             "error": "Failed to analyze case",
#             "details": str(e)
#         }), 500

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=5000, debug=True)



import os
import json
import re
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

# --- LangChain & Google Generative AI Imports ---
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain.prompts import ChatPromptTemplate
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA

# Load environment variables
load_dotenv()

# --- App Initialization ---
app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000"}})

# --- LLM Initialization ---
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash-preview-05-20",
    temperature=0.3,
    google_api_key=os.getenv("GOOGLE_API_KEY")
)

# --- RAG Chain Cache ---
rag_chain_cache = {}

def get_rag_chain():
    """Initialize and cache RAG chain for legal documents."""
    if "rag_chain" in rag_chain_cache:
        return rag_chain_cache["rag_chain"]

    # Embeddings
    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/embedding-001",
        google_api_key=os.getenv("GOOGLE_API_KEY")
    )

    # Load legal document
    kb_path = "./knowledge_base/payment_of_wages_act.txt"
    if not os.path.exists(kb_path):
        raise FileNotFoundError(f"{kb_path} not found!")

    loader = TextLoader(kb_path)
    docs = loader.load()

    # Split into chunks
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    split_docs = splitter.split_documents(docs)

    # Vector store
    vector_store = FAISS.from_documents(split_docs, embeddings)
    retriever = vector_store.as_retriever()

    # Create RetrievalQA chain
    rag_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
        return_source_documents=True
    )
    rag_chain_cache["rag_chain"] = rag_chain
    return rag_chain

def clean_text_formatting(text):
    """Clean up numbered lists and formatting issues in text."""
    if not isinstance(text, str):
        return text
    
    # Remove numbered list patterns like "1. ", "2. ", etc.
    text = re.sub(r'\d+\.\s+\*\*([^*]+)\*\*:\s*', r'\1: ', text)
    text = re.sub(r'\d+\.\s+', '', text)
    
    # Remove markdown bold formatting
    text = re.sub(r'\*\*([^*]+)\*\*', r'\1', text)
    
    # Clean up multiple spaces and newlines
    text = re.sub(r'\s+', ' ', text)
    text = text.strip()
    
    return text

def parse_json_from_response(content):
    """Helper function to extract JSON from LLM response."""
    try:
        # First try direct parsing
        parsed = json.loads(content)
    except json.JSONDecodeError:
        # Try to extract JSON from markdown code blocks
        json_match = re.search(r'```json\s*(.*?)\s*```', content, re.DOTALL)
        if json_match:
            try:
                parsed = json.loads(json_match.group(1))
            except json.JSONDecodeError:
                pass
        else:
            # Try to find any JSON object in the text
            json_match = re.search(r'(\{.*\})', content, re.DOTALL)
            if json_match:
                try:
                    parsed = json.loads(json_match.group(1))
                except json.JSONDecodeError:
                    pass
            else:
                raise ValueError("Could not parse JSON from LLM response")
    
    # Clean up text formatting in the parsed JSON
    if isinstance(parsed, dict):
        for key, value in parsed.items():
            if isinstance(value, str):
                parsed[key] = clean_text_formatting(value)
            elif isinstance(value, list):
                for i, item in enumerate(value):
                    if isinstance(item, dict):
                        for sub_key, sub_value in item.items():
                            if isinstance(sub_value, str):
                                item[sub_key] = clean_text_formatting(sub_value)
    
    return parsed

# --- API Endpoints ---

@app.route('/api/know-your-rights', methods=['POST'])
def know_your_rights():
    data = request.get_json()
    if not data or 'query' not in data:
        return jsonify({"error": "No query provided"}), 400

    try:
        # Temporary workaround: Use general legal knowledge instead of RAG
        # due to Google embedding API quota limits
        formatting_prompt = f"""
        You are a legal expert with knowledge of employment law, particularly the Payment of Wages Act. 
        Answer the user's question about their legal rights and format your response into this exact JSON structure:
        
        {{
            "explanation": "A simple, plain-language explanation of the user's rights based on general legal principles",
            "relevantLaws": [
                {{
                    "title": "The title of the relevant law or legal principle",
                    "text": "A simple explanation of what the law means"
                }}
            ],
            "guidance": "Actionable guidance or next steps for the user - write as flowing paragraphs, NOT as numbered lists or bullet points",
            "disclaimer": "This is for informational purposes only and does not constitute legal advice. Please consult with a qualified attorney for personalized legal advice."
        }}
        
        IMPORTANT FORMATTING RULES:
        - For "guidance": Write in paragraph form, not numbered lists or bullet points
        - Use natural language flow with proper sentences
        - Separate different advice points with periods, not numbers or bullets
        - Keep all text clean and readable for web display
        
        User's question: {data['query']}
        
        Focus on employment rights, wage payment laws, and worker protections. Provide practical, actionable advice.
        Respond with ONLY the JSON, no additional text:
        """
        
        response = llm.invoke([{"role": "user", "content": formatting_prompt}])
        content = response.content if hasattr(response, "content") else str(response)
        
        parsed_response = parse_json_from_response(content)
        return jsonify(parsed_response)
        
    except Exception as e:
        print(f"Error in know_your_rights: {str(e)}")
        return jsonify({"error": f"Failed to process rights query: {str(e)}"}), 500

@app.route('/api/simplify', methods=['POST'])
def simplify_document():
    data = request.get_json()
    if not data or 'text' not in data:
        return jsonify({"error": "No text provided"}), 400

    prompt_text = f"""
    You are an expert legal assistant. Simplify the following legal text into a JSON response with this exact structure:
    
    {{
        "summary_points": [
            {{
                "title": "A short, clear title for the point",
                "text": "The simplified explanation of the point"
            }}
        ]
    }}
    
    Legal Text to simplify:
    {data['text']}
    
    Respond with ONLY the JSON, no additional text:
    """

    try:
        response = llm.invoke([{"role": "user", "content": prompt_text}])
        content = response.content if hasattr(response, "content") else str(response)
        
        print("Raw LLM response:", content)  # Debug log
        
        parsed_response = parse_json_from_response(content)
        
        # Validate the response structure
        if "summary_points" not in parsed_response or not isinstance(parsed_response["summary_points"], list):
            raise ValueError("Missing 'summary_points' key or invalid format")

        return jsonify(parsed_response)

    except Exception as e:
        print(f"Error in simplify_document: {str(e)}")
        return jsonify({
            "error": "Failed to simplify document",
            "details": str(e)
        }), 500
        
@app.route("/api/advise", methods=["POST"])
def advise_case():
    data = request.get_json()
    if not data or 'case_text' not in data:
        return jsonify({"error": "No case text provided"}), 400
    
    case_text = data.get("case_text", "").strip()
    if not case_text:
        return jsonify({"error": "Case text is empty"}), 400

    prompt_text = f"""
    You are an AI Legal Advisor. Analyze the user's situation and provide a JSON response with this exact structure:
    
    {{
        "analysis_points": [
            {{
                "type": "point",
                "title": "A short, clear title for the legal point",
                "text": "The detailed explanation of the legal point"
            }},
            {{
                "type": "recommendation", 
                "title": "A short, clear title for the recommendation",
                "text": "The detailed explanation of the recommendation"
            }}
        ]
    }}
    
    Each item must have "type" as either "point" (for legal analysis) or "recommendation" (for actionable advice).
    Provide multiple points and recommendations as relevant.
    
    User's case:
    {case_text}
    
    Respond with ONLY the JSON, no additional text:
    """

    try:
        response = llm.invoke([{"role": "user", "content": prompt_text}])
        content = response.content if hasattr(response, "content") else str(response)
        
        print("Raw LLM response:", content)  # Debug log
        
        parsed_response = parse_json_from_response(content)
        
        # Validate the response structure
        if "analysis_points" not in parsed_response or not isinstance(parsed_response["analysis_points"], list):
            raise ValueError("Missing 'analysis_points' key or invalid format")
        
        # Validate each analysis point
        for point in parsed_response["analysis_points"]:
            if not all(key in point for key in ["type", "title", "text"]):
                raise ValueError("Invalid analysis point structure")
            if point["type"] not in ["point", "recommendation"]:
                raise ValueError("Invalid analysis point type")

        return jsonify(parsed_response)
        
    except Exception as e:
        print(f"Error in advise_case: {str(e)}")
        return jsonify({
            "error": "Failed to analyze case",
            "details": str(e)
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)