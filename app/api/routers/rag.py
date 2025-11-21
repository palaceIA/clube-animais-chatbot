from fastapi import APIRouter, HTTPException
from app.services.knowledge import knowledge_service
from app.services.rag import SearchSimilarity
from app.api.models.input import Input

router_rag = APIRouter(prefix="/rag", tags=["RAG - Retrieval-augmented generation"])


@router_rag.post("/ingest")
async def ingest_default_json():
    items = knowledge_service.load_json_file(knowledge_service.DATA_JSON)

    if not items:
        raise HTTPException(status_code=400, detail="Nenhum dado encontrado no JSON local.")

    knowledge_service.insert_rag_batch(items)

    return {
        "status": "success",
        "ingested": len(items)
    }


@router_rag.post("/search")
async def search_similariry(request: Input):
    results = SearchSimilarity.similarity(request.query)
    return {"matches": results}
