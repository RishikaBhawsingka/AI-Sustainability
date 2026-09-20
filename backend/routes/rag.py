from fastapi import APIRouter
from backend.services.rag_service import retrieve

router = APIRouter()


@router.get("/rag/search")
def rag_search(query: str):

    results = retrieve(query)

    return {
        "query": query,
        "results": results
    }