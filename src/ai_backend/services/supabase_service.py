import re
import json

from ai_backend.config import SUPABASE_URL, SUPABASE_PRIVATE_KEY

from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import SupabaseVectorStore
from supabase import create_client
from langchain_openai import ChatOpenAI

supabase_client = create_client(SUPABASE_URL, SUPABASE_PRIVATE_KEY)

embeddings = OpenAIEmbeddings()

vectorstore = SupabaseVectorStore(
    client=supabase_client,
    embedding=embeddings,
    table_name="documents",
    query_name="match_documents",
)

llm = ChatOpenAI(model_name="gpt-4o", temperature=0.5)


def extract_json(response_text):
    """Extract JSON content from Markdown-formatted response."""
    match = re.search(r"```json\n([\s\S]+?)\n```", response_text)
    if match:
        return match.group(1)
    return response_text


def store_document(text: str):
    vectorstore.add_texts([text])
    return {"message": "Document stored successfully"}


def query_document(query: str):
    results = vectorstore.similarity_search(query, k=3)
    return [doc.page_content for doc in results]


def retrieve_from_supabase(query: str):
    """Retrieves relevant documents from Supabase using vector similarity search."""
    retriever = vectorstore.as_retriever()

    try:
        retrieved_docs = retriever.invoke(query)
        return retrieved_docs
    except Exception as e:
        print(f"🚨 Error retrieving from Supabase: {e}")
        return []  # Return an empty list instead of crashing


def generate_rag_response(query: str):
    retrieved_docs = retrieve_from_supabase(query)
    context = "\n".join([doc.page_content for doc in retrieved_docs])

    prompt = f"""
    Use the provided context to answer the user's question in a structured JSON format.

    Context:
    {context}

    User Query: {query}

    Return the response as JSON:
    {{
        "query": "{query}",
        "answer": "<your generated answer>",
        "sources": [
            {{"title": "<source title>", "url": "<source URL>"}},
            {{"title": "<source title>", "url": "<source URL>"}}
        ]
    }}
    """

    response = llm.invoke(prompt)

    # ✅ Debugging step: Print response before parsing
    print(f"🔍 Raw LLM Response: {response.content}")

    if not response.content.strip():
        raise ValueError("OpenAI returned an empty response.")

    cleaned_response = extract_json(response.content)

    # ✅ Extract and parse JSON
    try:
        return json.loads(cleaned_response)
    except json.JSONDecodeError as e:
        raise ValueError(f"Failed to parse JSON response: {response.content}") from e
