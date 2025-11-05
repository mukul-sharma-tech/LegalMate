# rag_legal.py

import os
from typing import List
from pydantic import BaseModel, Field

# --- LangChain & Google Generative AI Imports ---
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema.runnable import RunnablePassthrough
from langchain.schema.output_parser import StrOutputParser

# --- Pydantic Models for All API Endpoints ---
# Using camelCase directly to avoid alias issues with LangChain

class RelevantLaw(BaseModel):
    title: str = Field(description="The title of the relevant law or legal principle")
    text: str = Field(description="A simple explanation of what the law means")

class KnowYourRightsResponse(BaseModel):
    explanation: str = Field(description="A simple, plain-language explanation of the user's rights based on the user's question.")
    relevantLaws: List[RelevantLaw] = Field(description="A list of relevant laws or principles.")
    guidance: str = Field(description="Actionable guidance for the user, written in paragraph form.")
    disclaimer: str = Field(
        description="This is for informational purposes only and does not constitute legal advice. Consult with a qualified attorney.", 
        default="This is for informational purposes only and does not constitute legal advice. Consult with a qualified attorney."
    )

class SimplifiedPoint(BaseModel):
    title: str = Field(description="A short, clear title for the point")
    text: str = Field(description="The simplified explanation of the point")

class SimplifyResponse(BaseModel):
    summaryPoints: List[SimplifiedPoint] = Field(description="List of simplified points from the document")

class AnalysisPoint(BaseModel):
    type: str = Field(description="Must be 'point' for legal analysis or 'recommendation' for advice.")
    title: str = Field(description="A short, clear title for the point or recommendation")
    text: str = Field(description="The detailed explanation of the point or recommendation")

class AdviseResponse(BaseModel):
    analysisPoints: List[AnalysisPoint] = Field(description="List of analysis points and recommendations")


# --- The Main "LLM" Class (No RAG) ---

class LegalRAG:
    def __init__(self, api_key: str):
        if not api_key:
            raise ValueError("Google API Key is required")
        
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.0-flash-exp", 
            temperature=0.3, 
            google_api_key=api_key
        )
        
        self.string_parser = StrOutputParser()

    # --- Public Methods for Each API Endpoint ---

    def get_rights(self, question: str) -> KnowYourRightsResponse:
        """Handler for the 'Know Your Rights' feature (without RAG)."""
        
        prompt = ChatPromptTemplate.from_template(
            """
            You are a helpful legal assistant. Answer the user's question based on your general knowledge.
            Provide a clear explanation, cite relevant legal principles, and give actionable guidance.

            **CRITICAL**: You MUST respond in the *same language* as the "User's Question".
            If the question is in Hindi, your answer MUST be in Hindi.

            User's Question: {question}
            """
        )
        structured_llm = self.llm.with_structured_output(KnowYourRightsResponse)
        
        chain = (
            {"question": RunnablePassthrough()}
            | prompt
            | structured_llm
        )
        return chain.invoke(question)

    def simplify_document(self, doc_text: str) -> SimplifyResponse:
        """Handler for the 'Simplify Document' feature (without RAG)."""
        
        prompt = ChatPromptTemplate.from_template(
            """
            You are an expert legal assistant. Your task is to simplify the 'User's Document' provided below.
            Break it down into simple, easy-to-understand points.

            **CRITICAL**: You MUST respond in the *same language* as the "User's Document".
            If the document is in Hindi, your summary points MUST be in Hindi.

            User's Document to Simplify:
            {document}
            """
        )
        structured_llm = self.llm.with_structured_output(SimplifyResponse)
        
        chain = (
            {"document": RunnablePassthrough()}
            | prompt
            | structured_llm
        )
        return chain.invoke(doc_text)

    def advise_on_case(self, case_text: str) -> AdviseResponse:
        """Handler for the 'AI Legal Advisor' feature."""
        
        prompt = ChatPromptTemplate.from_template(
            """
            You are an AI Legal Advisor. Analyze the user's situation described in 'User's Case'.
            Provide grounded, accurate analysis and actionable recommendations based on general legal principles.

            **CRITICAL**: You MUST respond in the *same language* as the "User's Case".
            If the case text is in Hindi, your analysis MUST be in Hindi.

            User's Case:
            {case}
            """
        )
        structured_llm = self.llm.with_structured_output(AdviseResponse)
        
        chain = (
            {"case": RunnablePassthrough()}
            | prompt
            | structured_llm
        )
        return chain.invoke(case_text)

    def ask_question_about_document(self, doc_text: str, question: str) -> str:
        """Handler for the 'Vakil' chatbot."""
        
        prompt = ChatPromptTemplate.from_template(
            """
            You are a helpful legal assistant named 'Vakil'. 
            A user has provided you with the following document and has a question about it.
            Answer the user's question based *only* on the document's contents.

            **CRITICAL**: You MUST respond in the *same language* as the "User's Question".
            If the question is in Hindi, your answer MUST be in Hindi.

            --- DOCUMENT ---
            {document}
            --- END DOCUMENT ---

            User's Question: {question}
            """
        )
        
        chain = (
            prompt
            | self.llm
            | self.string_parser
        )
        
        return chain.invoke({
            "document": doc_text,
            "question": question
        })
