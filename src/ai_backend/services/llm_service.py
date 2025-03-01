from langchain_openai import ChatOpenAI
from ai_backend.config import OPENAI_API_KEY
from langsmith import trace

# Initialize OpenAI LLM
llm = ChatOpenAI(model_name="gpt-4", temperature=0.7, api_key=OPENAI_API_KEY)


def generate_response(prompt: str):
    """Generate a response using OpenAI LLM."""
    with trace(name="generate_response"):
        return llm.invoke(prompt)
