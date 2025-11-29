# main.py

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import os

from vector_store import VectorStore, read_docs
from prompt_builder import build_prompt
from ollama_client import ollama_chat


app = FastAPI(title="Ollama RAG Chat")

# Static frontend
app.mount("/static", StaticFiles(directory="static"), name="static")


# ----- Environment variables -----
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "gemma3:4b")
DOC_DIR = os.getenv("DOC_DIR", os.path.join("data/docs"))
EMBED_MODEL = os.getenv("EMBED_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
TOP_K = int(os.getenv("TOP_K", "4"))

RAG_ENABLED = os.getenv("RAG_ENABLED", "true").lower() == "true"
VS = VectorStore(EMBED_MODEL)
VS.build(read_docs(DOC_DIR))


class ChatRequest(BaseModel):
    query: str
    top_k: int | None = None
    max_tokens: int | None = 384


class ChatResponse(BaseModel):
    answer: str
    retrieved: list


@app.get("/health")
def health():
    import requests
    try:
        ok = requests.get(f"{OLLAMA_URL}/api/tags", timeout=2).ok
    except:
        ok = False
    return {"status": "ok", "ollama": ok, "model": OLLAMA_MODEL}


@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    try:
        # RAG OFF → direct chat
        if True:
            answer = ollama_chat(
                OLLAMA_URL,
                OLLAMA_MODEL,
                "You are a helpful assistant.",
                req.query,
                max_tokens=req.max_tokens or 384
            )
            return ChatResponse(answer=answer, retrieved=[])

        retrieved = VS.search(req.query, top_k=req.top_k or TOP_K)
        system_prompt = "Use ONLY the provided context. Cite chunk ids like [#1]."
        prompt = build_prompt(req.query, retrieved)
        answer = ollama_chat(
            OLLAMA_URL,
            OLLAMA_MODEL,
            system_prompt,
            prompt,
            max_tokens=req.max_tokens or 384
        )
        return ChatResponse(answer=answer, retrieved=retrieved)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ollama error: {e}")
