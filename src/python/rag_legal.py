import os
from pydantic import BaseModel, Field

# --- LangChain & Google Generative AI Imports ---
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema.runnable import RunnablePassthrough
from langchain.schema.output_parser import StrOutputParser

# --- Pydantic Models (Pydantic v2 Syntax) ---

class RelevantLaw(BaseModel):
    title: str = Field(description="The title of the relevant law or legal principle")
    text: str = Field(description="A simple explanation of what the law means")

class KnowYourRightsResponse(BaseModel):
    explanation: str = Field(description="A simple, plain-language explanation...")
    relevantLaws: list[RelevantLaw] = Field(
        description="A list of relevant laws or principles.",
        default_factory=list  # Correct way to define a list
    )
    guidance: str = Field(description="Actionable guidance for the user.")
    disclaimer: str = Field(
        default="This is for informational purposes only and does not constitute legal advice. Consult with a qualified attorney."
    )

class SimplifiedPoint(BaseModel):
    title: str = Field(description="A short, clear title for the point")
    text: str = Field(description="The simplified explanation of the point")

class SimplifyResponse(BaseModel):
    summary_points: list[SimplifiedPoint] = Field(
        description="List of simplified points.",
        default_factory=list  # Correct way to define a list
    )

class AnalysisPoint(BaseModel):
    type: str = Field(description="Must be 'point' for analysis or 'recommendation' for advice.")
    title: str = Field(description="A short, clear title for the point")
    text: str = Field(description="The detailed explanation")

class AdviseResponse(BaseModel):
    analysis_points: list[AnalysisPoint] = Field(
        description="List of analysis points and recommendations.",
        default_factory=list  # Correct way to define a list
    )

# --- The Main Logic Class ---

class LegalRAG:
    def __init__(self, api_key: str):
        if not api_key:
            raise ValueError("Google API Key is required for LegalRAG")
            
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",  # Using a stable, public model
            temperature=0.3, 
            google_api_key=api_key
        )
        self.string_parser = StrOutputParser()

    # --- Method 1: Know Your Rights ---
    def get_rights(self, question: str) -> KnowYourRightsResponse:
        prompt = ChatPromptTemplate.from_template(
            """
            You are a helpful legal assistant. Answer based on general knowledge.
            Provide a clear explanation, cite relevant legal principles, and give actionable guidance.
            **CRITICAL**: Respond in the *same language* as the "User's Question".
            User's Question: {question}
            """
        )
        structured_llm = self.llm.with_structured_output(KnowYourRightsResponse)
        chain = {"question": RunnablePassthrough()} | prompt | structured_llm
        return chain.invoke(question)

    # --- Method 2: Simplify Document ---
    def simplify_document(self, doc_text: str) -> SimplifyResponse:
        prompt = ChatPromptTemplate.from_template(
            """
            You are an expert legal assistant. Simplify the 'User's Document' into easy-to-understand points.
            **CRITICAL**: Respond in the *same language* as the "User's Document".
            User's Document:
            {document}
            """
        )
        structured_llm = self.llm.with_structured_output(SimplifyResponse)
        chain = {"document": RunnablePassthrough()} | prompt | structured_llm
        return chain.invoke(doc_text)

    # --- Method 3: Advise on Case ---
    def advise_on_case(self, case_text: str) -> AdviseResponse:
        prompt = ChatPromptTemplate.from_template(
            """
            You are an AI Legal Advisor. Analyze the 'User's Case'.
            Provide grounded analysis and actionable recommendations.
            **CRITICAL**: Respond in the *same language* as the "User's Case".
            User's Case:
            {case}
            """
        )
        structured_llm = self.llm.with_structured_output(AdviseResponse)
        chain = {"case": RunnablePassthrough()} | prompt | structured_llm
        return chain.invoke(case_text)

    # --- Method 4: Ask Vakil (Chatbot) ---
    def ask_question_about_document(self, doc_text: str, question: str) -> str:
        prompt = ChatPromptTemplate.from_template(
            """
            You are 'Vakil', a helpful legal assistant. 
            Answer the user's question based *only* on the document's contents.
            **CRITICAL**: Respond in the *same language* as the "User's Question".

            --- DOCUMENT ---
            {document}
            --- END DOCUMENT ---

            User's Question: {question}
            """
        )
        chain = prompt | self.llm | self.string_parser
        return chain.invoke({
            "document": doc_text,
            "question": question
        })
