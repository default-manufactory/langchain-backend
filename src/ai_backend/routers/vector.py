from fastapi import APIRouter
from pydantic import BaseModel
from ai_backend.services.supabase_service import store_document, query_document

router = APIRouter()


class DocumentRequest(BaseModel):
    text: str


class QueryRequest(BaseModel):
    query: str


@router.post("/store/")
def store_document_api(request: DocumentRequest):
    """Store document embeddings in Supabase."""
    return store_document(request.text)


@router.post("/query/")
def query_document_api(request: QueryRequest):
    """Retrieve relevant documents from Supabase."""
    return query_document(request.query)
