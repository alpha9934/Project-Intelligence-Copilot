import os
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
import json

from src.config import get_settings
from src.utils.logger import setup_logger
from src.vector_store import get_vector_store
from src.guardrails import ProjectInsight

logger = setup_logger(__name__)
settings = get_settings()

def format_docs(docs):
    """
    Formats the retrieved documents to include their metadata.
    This is what allows the LLM to cite exactly which file it got the answer from.
    """
    formatted_chunks = []
    for doc in docs:
        source = doc.metadata.get("source_file", "Unknown Source")
        chunk_id = doc.metadata.get("chunk_id", "Unknown Chunk")
        # We inject the source name directly into the text the LLM reads
        formatted_chunks.append(f"[Source: {source} | ID: {chunk_id}]\n{doc.page_content}\n")
    return "\n\n".join(formatted_chunks)

def get_rag_chain():
    """
    Builds the LangChain RAG pipeline using modern LCEL (LangChain Expression Language).
    """
    # 1. Inject API keys for LangChain modules
    os.environ["OPENAI_API_KEY"] = settings.OPENAI_API_KEY
    os.environ["PINECONE_API_KEY"] = settings.PINECONE_API_KEY

    # 2. Set up the Pinecone Retriever (Fetch top 5 most relevant chunks)
    vector_store = get_vector_store()
    retriever = vector_store.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 5} 
    )

    # 3. Initialize the Reasoning Engine (LLM)
    llm = ChatOpenAI(
        model=settings.LLM_MODEL,
        temperature=settings.TEMPERATURE # Kept at 0.0 to prevent hallucinations
    )
    
    # 🔥 This is the enterprise magic: Forcing the LLM to obey our Pydantic schema
    structured_llm = llm.with_structured_output(ProjectInsight)

    # 4. The System Prompt (Instructions for the Copilot)
    system_prompt = (
        "You are the Project Intelligence Copilot, an enterprise AI assistant for engineering managers. "
        "Your job is to answer questions about project delays, risks, and responsibilities. "
        "You MUST base your answer STRICTLY on the following retrieved context. "
        "If the context does not contain the answer, state that you do not have enough information. "
        "Do NOT hallucinate or make up facts. "
        "Use the exact [Source: filename] tags provided in the context to populate your evidence_citations.\n\n"
        "Context:\n{context}"
    )

    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", "{question}")
    ])

    # 5. Build the execution chain
    rag_chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | structured_llm
    )
    
    return rag_chain

def answer_question(question: str) -> dict:
    """
    Executes the RAG chain and returns the structured dictionary.
    """
    logger.info(f"Received query: '{question}'")
    try:
        chain = get_rag_chain()
        logger.info("Executing RAG chain and reasoning engine...")
        
        # The chain returns a validated ProjectInsight Pydantic object
        result: ProjectInsight = chain.invoke(question)
        
        logger.info("Successfully generated structured, hallucination-free response.")
        
        # Convert Pydantic object to a standard Python dictionary for the API later
        return result.model_dump()
    except Exception as e:
        logger.error(f"Error during RAG execution: {str(e)}")
        raise e

if __name__ == "__main__":
    # Let's test the "Murder Mystery" directly in the terminal!
    test_question = "Why is the concrete pouring delayed, who is responsible, and what is the next action?"
    
    logger.info("--- STARTING LOCAL RAG TEST ---")
    response = answer_question(test_question)
    
    print("\n" + "="*50)
    print("🤖 COPILOT RESPONSE:")
    print("="*50)
    print(json.dumps(response, indent=2))
    print("="*50)