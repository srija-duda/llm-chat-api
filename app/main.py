import asyncio

from fastapi import FastAPI, HTTPException

from app.config import AVAILABLE_MODELS, DEFAULT_PRICE_PER_1000
from app.models import ChatResponse, ChatRequest

app = FastAPI(title="LLM Chat API", version="1.0.0")
@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/models")
def list_models():
    return {"models": AVAILABLE_MODELS}

@app.get("/models/{name}")
def get_model(name: str):
    if name not in AVAILABLE_MODELS:
        raise HTTPException(status_code=404, detail=f"Model '{name}' not found")
    return {"model": name, "available": True}

@app.get("/cost")
def calculate_cost(tokens: int, price_per_1000: float = DEFAULT_PRICE_PER_1000):
    return {"tokens": tokens, "cost": tokens * price_per_1000 / 1000}

@app.post("/chat", response_model=ChatResponse, responses={400: {"description": "Model not supported"}})
async def chat(request: ChatRequest):
    if request.model not in AVAILABLE_MODELS:
        raise HTTPException(status_code=400, detail=f"Model '{request.model}' is not supported")
    await asyncio.sleep(1)
    return ChatResponse(
        model=request.model,
        answer=f"Simulated answer to '{request.question}' using model '{request.model}'",
        tokens_used=len(request.question.split())
    )

