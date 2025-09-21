# rag_legal.py

import os
from typing import List
from pydantic.v1 import BaseModel, Field

# --- LangChain & Google Generative AI Imports ---
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain.prompts import ChatPromptTemplate
from langchain_community.document_loaders import TextLoader, DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain.schema.runnable import RunnablePassthrough, RunnableParallel
from langchain.schema import Document

# --- Pydantic Models for All API Endpoints ---

# For /know-your-rights
class RelevantLaw(BaseModel):
    title: str = Field(description="The title of the relevant law or legal principle")
    text: str = Field(description="A simple explanation of what the law means")

class KnowYourRightsResponse(BaseModel):
    explanation: str = Field(description="A simple, plain-language explanation of the user's rights based on the provided context.")
    relevantLaws: List[RelevantLaw] = Field(description="A list of relevant laws or principles from the context.")
    guidance: str = Field(description="Actionable guidance for the user, written in paragraph form.")
    disclaimer: str = Field(description="Standard disclaimer...", default="This is for informational purposes only and does not constitute legal advice. Consult with a qualified attorney.")

# For /simplify
class SimplifiedPoint(BaseModel):
    title: str = Field(description="A short, clear title for the point")
    text: str = Field(description="The simplified explanation of the point")

class SimplifyResponse(BaseModel):
    summary_points: List[SimplifiedPoint]

# For /advise
class AnalysisPoint(BaseModel):
    type: str = Field(description="Must be 'point' for legal analysis or 'recommendation' for advice.")
    title: str = Field(description="A short, clear title for the point or recommendation")
    text: str = Field(description="The detailed explanation of the point or recommendation")

class AdviseResponse(BaseModel):
    analysis_points: List[AnalysisPoint]


# --- The Main RAG Class ---

class LegalRAG:
    def __init__(self, knowledge_base_path: str, api_key: str):
        self.kb_path = knowledge_base_path
        
        # --- Core Components Initialized Once ---
        self.llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash-latest", temperature=0.3, google_api_key=api_key)
        
        docs = self._load_documents()
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
        split_docs = text_splitter.split_documents(docs)
        
        self.vectorstore = self._create_vectorstore(split_docs, api_key)
        self.retriever = self.vectorstore.as_retriever(search_kwargs={"k": 3})

    # --- Private Helper Methods ---
    def _load_documents(self) -> List[Document]:
        loader = DirectoryLoader(self.kb_path, glob="**/*.txt", loader_cls=TextLoader)
        return loader.load()

    def _create_vectorstore(self, split_docs: List[Document], api_key: str) -> FAISS:
        embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001", google_api_key=api_key)
        return FAISS.from_documents(split_docs, embeddings)

    def _format_docs(self, docs: List[Document]) -> str:
        return "\n\n".join([f"--- Source: {doc.metadata.get('source', 'N/A')} ---\n{doc.page_content}" for doc in docs])

    # --- Public Methods for Each API Endpoint ---

    def get_rights(self, question: str) -> KnowYourRightsResponse:
        """Handler for the 'Know Your Rights' feature."""
        prompt = ChatPromptTemplate.from_template(
            """
            You are a helpful legal assistant. Using the following legal context, answer the user's question.
            Provide a clear explanation, cite relevant laws from the context, and give actionable guidance.
            If the context does not contain the answer, state that you cannot answer based on the available information.

            Context: {context}
            User's Question: {question}
            """
        )
        structured_llm = self.llm.with_structured_output(KnowYourRightsResponse)
        
        chain = (
            {"context": self.retriever | self._format_docs, "question": RunnablePassthrough()}
            | prompt
            | structured_llm
        )
        return chain.invoke(question)

    def simplify_document(self, doc_text: str) -> SimplifyResponse:
        """Handler for the 'Simplify Document' feature."""
        prompt = ChatPromptTemplate.from_template(
            """
            You are an expert legal assistant. Your task is to simplify the 'User's Document' provided below.
            Use the 'Legal Context' retrieved from our knowledge base to ensure your simplification is accurate, legally sound, and explains key terms correctly.

            Legal Context:
            {context}

            User's Document to Simplify:
            {document}
            """
        )
        structured_llm = self.llm.with_structured_output(SimplifyResponse)
        
        # We retrieve context based on the document's content
        chain = (
            RunnableParallel(
                context=(RunnablePassthrough() | self.retriever | self._format_docs),
                document=RunnablePassthrough()
            )
            | prompt
            | structured_llm
        )
        return chain.invoke(doc_text)

    def advise_on_case(self, case_text: str) -> AdviseResponse:
        """Handler for the 'AI Legal Advisor' feature."""
        prompt = ChatPromptTemplate.from_template(
            """
            You are an AI Legal Advisor. Analyze the user's situation described in 'User's Case'.
            Use the retrieved 'Legal Context' to provide grounded, accurate analysis and actionable recommendations. Your advice must be based on the provided legal text.

            Legal Context:
            {context}

            User's Case:
            {case}
            """
        )
        structured_llm = self.llm.with_structured_output(AdviseResponse)
        
        chain = (
            {"context": self.retriever | self._format_docs, "case": RunnablePassthrough()}
            | prompt
            | structured_llm
        )
        return chain.invoke(case_text)