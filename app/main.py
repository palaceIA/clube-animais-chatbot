from fastapi import FastAPI
from app.api.routers.rag import router_rag 
from app.api.routers.chat import router_agent 


app = FastAPI(title="API - Chatbot clube dos animais")

app.include_router(router_agent)
app.include_router(router_rag)
