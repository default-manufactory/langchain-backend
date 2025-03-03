from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import SupabaseVectorStore
from supabase import create_client
from ai_backend.config import SUPABASE_URL, SUPABASE_PRIVATE_KEY

supabase_client = create_client(SUPABASE_URL, SUPABASE_PRIVATE_KEY)

embeddings = OpenAIEmbeddings()

vectorstore = SupabaseVectorStore(
    client=supabase_client,
    embedding=embeddings,
    table_name="documents",
    query_name="match_documents",
)


def store_document(text: str):
    vectorstore.add_texts([text])
    return {"message": "Document stored successfully"}


def query_document(query: str):
    results = vectorstore.similarity_search(query, k=3)
    return [doc.page_content for doc in results]
