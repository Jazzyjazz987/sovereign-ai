#!/usr/bin/env python3
"""
FastAPI server for Sovereign AI Stack (T1/T2 models via Ollama)
Run: uvicorn main_fastapi:app --reload --host 0.0.0.0 --port 5000
"""
from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import Optional
import logging
import asyncio
from api.ollama_client import OllamaClient

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Sovereign AI Stack API",
    description="T1/T2 Model Access via Ollama",
    version="1.0.0"
)

# Initialize client once (reuse connection)
try:
    client = OllamaClient()
    logger.info("✅ FastAPI initialized with Ollama client")
except Exception as e:
    logger.warning(f"⚠️  Ollama connection warning: {e}")
    client = None


class QueryRequest(BaseModel):
    """Query request model."""
    model: str = "t1"
    prompt: str
    system: Optional[str] = None


class QueryResponse(BaseModel):
    """Query response model."""
    model: str
    prompt: str
    response: str
    latency_estimate: str


@app.get("/health")
async def health():
    """Health check endpoint."""
    try:
        if client:
            return {"status": "healthy", "service": "sovereign-ai-api"}
        return {"status": "warning", "service": "sovereign-ai-api", "message": "Ollama not connected"}
    except Exception as e:
        return {"status": "unhealthy", "error": str(e)}, 503


@app.get("/models")
async def list_models():
    """List available models."""
    if not client:
        raise HTTPException(status_code=503, detail="Ollama client not initialized")

    models = []
    for key, config in client.MODELS.items():
        models.append({
            "key": key,
            "name": config.name,
            "display_name": config.display_name,
            "description": config.description,
            "latency": config.latency_estimate
        })
    return {"models": models}


@app.post("/query", response_model=QueryResponse)
async def query(request: QueryRequest):
    """Query a model synchronously."""
    if not client:
        raise HTTPException(status_code=503, detail="Ollama client not initialized")

    try:
        response = client.query(request.model, request.prompt, request.system)
        model_config = client.get_model_info(request.model)

        return QueryResponse(
            model=model_config["display_name"],
            prompt=request.prompt,
            response=response,
            latency_estimate=model_config["latency"]
        )
    except Exception as e:
        logger.error(f"Query error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/query-stream")
async def query_stream(request: QueryRequest):
    """Query a model with streaming response."""
    if not client:
        raise HTTPException(status_code=503, detail="Ollama client not initialized")

    async def stream_response():
        try:
            for chunk in client.query_stream(request.model, request.prompt, request.system):
                yield chunk.encode() + b"\n"
        except Exception as e:
            logger.error(f"Stream error: {e}")
            yield f"Error: {str(e)}".encode()

    return StreamingResponse(stream_response(), media_type="text/event-stream")


@app.post("/batch")
async def batch_query(requests: list[QueryRequest]):
    """Process multiple queries in batch."""
    if not client:
        raise HTTPException(status_code=503, detail="Ollama client not initialized")

    results = []
    for req in requests:
        try:
            response = client.query(req.model, req.prompt, req.system)
            results.append({
                "prompt": req.prompt,
                "response": response,
                "status": "success"
            })
        except Exception as e:
            results.append({
                "prompt": req.prompt,
                "error": str(e),
                "status": "failed"
            })

    return {"results": results, "total": len(requests), "succeeded": sum(1 for r in results if r["status"] == "success")}


@app.get("/info")
async def info():
    """API information."""
    return {
        "name": "Sovereign AI Stack API",
        "version": "1.0.0",
        "models": {
            "t1": "Mistral 7B (Fast, French support, 3-4s latency)",
            "t2": "Llama2 7B (Deep analysis, 4-5s latency)"
        },
        "endpoints": {
            "POST /query": "Synchronous query",
            "POST /query-stream": "Streaming response",
            "POST /batch": "Batch processing",
            "GET /models": "List models",
            "GET /health": "Health check"
        },
        "usage": {
            "simple": "POST /query with {\"model\": \"t1\", \"prompt\": \"Your question\"}",
            "streaming": "POST /query-stream for real-time responses",
            "batch": "POST /batch with array of queries"
        }
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000, log_level="info")
