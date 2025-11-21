from fastapi import APIRouter

from app.api.models.input import Input
from app.services.llm import agent

router_agent = APIRouter(
    prefix="/chat",
    tags=["ChatBot - Clube dos animais"]
)

@router_agent.post("/agent/rag")
async def response_agent_rag(request : Input) : 
    response = await agent.response_message(request.query)
    return {"response" : response}
    