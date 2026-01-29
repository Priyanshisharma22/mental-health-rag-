from fastapi import FastAPI
from pydantic import BaseModel
from rag_graph import run_rag

api = FastAPI(title="Mental Health RAG API")


class QueryRequest(BaseModel):
    query: str


@api.get("/health")
def health():
    return {"status": "ok"}


@api.post("/query")
def query(req: QueryRequest):
    return run_rag(req.query)
