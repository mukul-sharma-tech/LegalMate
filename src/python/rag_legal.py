# import os
# from typing import List
# from pydantic.v1 import BaseModel, Field

# # --- LangChain & Google Generative AI Imports ---
# from langchain_google_genai import ChatGoogleGenerativeAI
# from langchain.prompts import ChatPromptTemplate
# from langchain.schema.runnable import RunnablePassthrough
# from langchain.schema.output_parser import StrOutputParser # Import this

# # --- Pydantic Models for All API Endpoints ---
# # (These remain the same as before)

# class RelevantLaw(BaseModel):
#     title: str = Field(description="The title of the relevant law or legal principle")
#     text: str = Field(description="A simple explanation of what the law means")

# class KnowYourRightsResponse(BaseModel):
#     explanation: str = Field(description="A simple, plain-language explanation of the user's rights based on the user's question.")
#     relevantLaws: List[RelevantLaw] = Field(description="A list of relevant laws or principles.")
#     guidance: str = Field(description="Actionable guidance for the user, written in paragraph form.")
#     disclaimer: str = Field(description="Standard disclaimer...", default="This is for informational purposes only and does not constitute legal advice. Consult with a qualified attorney.")

# class SimplifiedPoint(BaseModel):
#     title: str = Field(description="A short, clear title for the point")
#     text: str = Field(description="The simplified explanation of the point")

# class SimplifyResponse(BaseModel):
#     summary_points: List[SimplifiedPoint]

# class AnalysisPoint(BaseModel):
#     type: str = Field(description="Must be 'point' for legal analysis or 'recommendation' for advice.")
#     title: str = Field(description="A short, clear title for the point or recommendation")
#     text: str = Field(description="The detailed explanation of the point or recommendation")

# class AdviseResponse(BaseModel):
#     analysis_points: List[AnalysisPoint]


# # --- The Main "LLM" Class (No RAG) ---

# class LegalRAG:
#     def __init__(self, api_key: str):
        
#         self.llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.3, google_api_key=api_key)
        
#         # --- Add a new simple output parser ---
#         self.string_parser = StrOutputParser()

#     # --- Public Methods for Each API Endpoint ---

#     def get_rights(self, question: str) -> KnowYourRightsResponse:
#         """Handler for the 'Know Your Rights' feature (without RAG)."""
        
#         # --- MODIFIED: Added language instruction ---
#         prompt = ChatPromptTemplate.from_template(
#             """
#             You are a helpful legal assistant. Answer the user's question based on your general knowledge.
#             Provide a clear explanation, cite relevant legal principles, and give actionable guidance.

#             **CRITICAL**: You MUST respond in the *same language* as the "User's Question".
#             If the question is in Hindi, your answer MUST be in Hindi.

#             User's Question: {question}
#             """
#         )
#         structured_llm = self.llm.with_structured_output(KnowYourRightsResponse)
        
#         chain = (
#             {"question": RunnablePassthrough()}
#             | prompt
#             | structured_llm
#         )
#         return chain.invoke(question)

#     def simplify_document(self, doc_text: str) -> SimplifyResponse:
#         """Handler for the 'Simplify Document' feature (without RAG)."""
        
#         # --- MODIFIED: Added language instruction ---
#         prompt = ChatPromptTemplate.from_template(
#             """
#             You are an expert legal assistant. Your task is to simplify the 'User's Document' provided below.
#             Break it down into simple, easy-to-understand points.

#             **CRITICAL**: You MUST respond in the *same language* as the "User's Document".
#             If the document is in Hindi, your summary points MUST be in Hindi.

#             User's Document to Simplify:
#             {document}
#             """
#         )
#         structured_llm = self.llm.with_structured_output(SimplifyResponse)
        
#         chain = (
#             {"document": RunnablePassthrough()}
#             | prompt
#             | structured_llm
#         )
#         return chain.invoke(doc_text)

#     def advise_on_case(self, case_text: str) -> AdviseResponse:
#         """Handler for the 'AI Legal Advisor' feature."""
        
#         # --- MODIFIED: Added language instruction ---
#         prompt = ChatPromptTemplate.from_template(
#             """
#             You are an AI Legal Advisor. Analyze the user's situation described in 'User's Case'.
#             Provide grounded, accurate analysis and actionable recommendations based on general legal principles.

#             **CRITICAL**: You MUST respond in the *same language* as the "User's Case".
#             If the case text is in Hindi, your analysis MUST be in Hindi.

#             User's Case:
#             {case}
#             """
#         )
#         structured_llm = self.llm.with_structured_output(AdviseResponse)
        
#         chain = (
#             {"case": RunnablePassthrough()}
#             | prompt
#             | structured_llm
#         )
#         return chain.invoke(case_text)

#     # --- This is the new method for your Vakil chatbot ---
#     def ask_question_about_document(self, doc_text: str, question: str) -> str:
#         """Handler for the 'Vakil' chatbot."""
        
#         # --- MODIFIED: Added language instruction ---
#         prompt = ChatPromptTemplate.from_template(
#             """
#             You are a helpful legal assistant named 'Vakil'. 
#             A user has provided you with the following document and has a question about it.
#             Answer the user's question based *only* on the document's contents.

#             **CRITICAL**: You MUST respond in the *same language* as the "User's Question".
#             If the question is in Hindi, your answer MUST be in Hindi.

#             --- DOCUMENT ---
#             {document}
#             --- END DOCUMENT ---

#             User's Question: {question}
#             """
#         )
        
#         chain = (
#             prompt
#             | self.llm
#             | self.string_parser
#         )
        
#         return chain.invoke({
#             "document": doc_text,
#             "question": question
#         })



import os
from typing import List
from pydantic import BaseModel, Field

# LangChain & Google Generative AI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema.runnable import RunnablePassthrough
from langchain.schema.output_parser import StrOutputParser


# ✅ Pydantic Models Corrected for Gemini Structured Output

class RelevantLaw(BaseModel):
    title: str
    text: str


class KnowYourRightsResponse(BaseModel):
    explanation: str
    relevantLaws: List[RelevantLaw] = Field(default_factory=list)
    guidance: str
    disclaimer: str = "This is for informational purposes only and does not constitute legal advice."


class SimplifiedPoint(BaseModel):
    title: str
    text: str


class SimplifyResponse(BaseModel):
    summary_points: List[SimplifiedPoint] = Field(default_factory=list)


class AnalysisPoint(BaseModel):
    type: str = Field(description="Must be 'point' or 'recommendation'")
    title: str
    text: str


class AdviseResponse(BaseModel):
    analysis_points: List[AnalysisPoint] = Field(default_factory=list)


class LegalRAG:
    def __init__(self, api_key: str):
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            temperature=0.3,
            google_api_key=api_key
        )
        self.string_parser = StrOutputParser()

    # ✅ 1️⃣ Know Your Rights
    def get_rights(self, question: str) -> KnowYourRightsResponse:
        prompt = ChatPromptTemplate.from_template(
            """
            You are a helpful legal assistant.

            CRITICAL:
            ✅ Respond in the SAME LANGUAGE as the question
            ✅ Provide rights, relevant laws, and guidance
            ✅ Keep disclaimer at the end

            User Question:
            {question}
            """
        )

        chain = (
            {"question": RunnablePassthrough()}
            | prompt
            | self.llm.with_structured_output(KnowYourRightsResponse)
        )
        return chain.invoke(question)

    # ✅ 2️⃣ Simplify Legal Document
    def simplify_document(self, doc_text: str) -> SimplifyResponse:
        prompt = ChatPromptTemplate.from_template(
            """
            You are a legal expert simplifying a legal document.

            Rules:
            ✅ Same language as the content
            ✅ Short bullet points, easy language

            Document:
            {document}
            """
        )

        chain = (
            {"document": RunnablePassthrough()}
            | prompt
            | self.llm.with_structured_output(SimplifyResponse)
        )
        return chain.invoke(doc_text)

    # ✅ 3️⃣ Legal Case Advisor
    def advise_on_case(self, case_text: str) -> AdviseResponse:
        prompt = ChatPromptTemplate.from_template(
            """
            You are a Legal Advisor AI.

            Rules:
            ✅ Same language as user
            ✅ Provide analysis + recommendations

            User Case:
            {case}
            """
        )

        chain = (
            {"case": RunnablePassthrough()}
            | prompt
            | self.llm.with_structured_output(AdviseResponse)
        )
        return chain.invoke(case_text)

    # ✅ 4️⃣ Vakil Chatbot (RAG ready — currently no DB)
    def ask_question_about_document(self, doc_text: str, question: str) -> str:
        prompt = ChatPromptTemplate.from_template(
            """
            You are VAKIL, a friendly legal assistant.

            ✅ Answer using only the document below
            ✅ Same language as question

            ---- DOCUMENT ----
            {document}
            ------------------

            User's Question: {question}
            """
        )

        chain = prompt | self.llm | self.string_parser
        return chain.invoke({"document": doc_text, "question": question})
