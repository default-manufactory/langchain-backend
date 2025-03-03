from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import SupabaseVectorStore
from supabase import create_client
from ai_backend.config import SUPABASE_URL, SUPABASE_PRIVATE_KEY

from langchain_openai import ChatOpenAI

supabase_client = create_client(SUPABASE_URL, SUPABASE_PRIVATE_KEY)

embeddings = OpenAIEmbeddings()

vectorstore = SupabaseVectorStore(
    client=supabase_client,
    embedding=embeddings,
    table_name="documents",
    query_name="match_documents",
)

llm = ChatOpenAI(model_name="gpt-4", temperature=0.5)


def store_document(text: str):
    vectorstore.add_texts([text])
    return {"message": "Document stored successfully"}


def query_document(query: str):
    results = vectorstore.similarity_search(query, k=3)
    return [doc.page_content for doc in results]


def retrieve_from_supabase(query: str):
    """Retrieves relevant documents from Supabase using vector similarity search."""
    retriever = vectorstore.as_retriever()  # Convert to a retriever tool
    retrieved_docs = retriever.get_relevant_documents(query)  # Search for relevant docs
    return retrieved_docs


def generate_rag_response(query: str):
    """Uses RAG (Retrieval-Augmented Generation) to generate a response."""
    retrieved_docs = retrieve_from_supabase(query)  # Retrieve docs

    context = "\n".join([doc.page_content for doc in retrieved_docs])

    # Construct prompt with retrieved data
    prompt = f"Use the following context to answer:\n\n{context}\n\nQuery: {query}"

    return llm.invoke(prompt)
