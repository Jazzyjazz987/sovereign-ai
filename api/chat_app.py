#!/usr/bin/env python3
"""
Chat Web Application with Intelligent Cascade Routing
Starts with T1 (fast), escalates to T2+ for complex queries
Run: python -m uvicorn api.chat_app:app --reload --port 5000
"""
from fastapi import FastAPI, WebSocket, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Optional
import logging
import json
import asyncio
from pathlib import Path
from api.cascade_router import CascadeRouter

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Sovereign AI Chat",
    description="Chat with T1→T2→T3+ cascade routing",
    version="1.0.0"
)

router = CascadeRouter()

# Mount static files
static_dir = Path(__file__).parent.parent / "static"
if static_dir.exists():
    app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")
    logger.info(f"✅ Static files mounted: {static_dir}")


class ChatMessage(BaseModel):
    """Chat message."""
    message: str
    force_model: Optional[str] = None  # Force T1/T2


@app.get("/")
async def root():
    """Serve chat UI."""
    return FileResponse("static/chat.html")


@app.get("/architecture")
async def architecture():
    """Serve architecture diagram."""
    return FileResponse("static/stack-architecture.html")


@app.post("/api/chat")
async def chat(msg: ChatMessage):
    """Non-streaming chat endpoint."""
    try:
        result = router.query(msg.message, msg.force_model)
        return {
            "response": result["response"],
            "model": result["model"],
            "tier": result["tier"],
            "reason": result["reason"],
        }
    except Exception as e:
        logger.error(f"Chat error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.websocket("/ws/chat")
async def websocket_chat(websocket: WebSocket):
    """WebSocket for streaming chat."""
    await websocket.accept()
    logger.info("✅ Client connected")

    try:
        while True:
            # Receive message
            data = await websocket.receive_text()
            msg = json.loads(data)
            prompt = msg.get("message")
            force_model = msg.get("force_model")

            if not prompt:
                continue

            logger.info(f"📨 Message: {prompt[:50]}...")

            # Select model
            if force_model:
                model_key = force_model
                tier = 1 if force_model == "t1" else 2
                reason = "forced"
            else:
                selection = router.select_model(prompt)
                model_key = selection["key"]
                tier = selection["tier"]
                reason = selection["reason"]

            # Send model selection
            await websocket.send_json({
                "type": "model_selected",
                "model": model_key,
                "tier": tier,
                "reason": reason,
                "complexity": router.calculate_complexity(prompt),
            })

            # Stream response
            await websocket.send_json({"type": "streaming_start"})

            full_response = ""
            try:
                for chunk in router.query_stream(prompt, force_model):
                    full_response += chunk
                    await websocket.send_json({
                        "type": "chunk",
                        "data": chunk,
                    })
                    # Small delay to prevent overwhelming
                    await asyncio.sleep(0.01)
            except Exception as e:
                logger.error(f"Stream error: {e}")
                await websocket.send_json({
                    "type": "error",
                    "message": str(e),
                })

            # Send completion
            await websocket.send_json({
                "type": "streaming_complete",
                "total_length": len(full_response),
            })

    except Exception as e:
        logger.error(f"WebSocket error: {e}")
    finally:
        await websocket.close()
        logger.info("❌ Client disconnected")


@app.get("/api/models")
async def get_models():
    """List available models."""
    return {
        "models": [
            {
                "key": "t1",
                "name": "Mistral 7B",
                "tier": 1,
                "description": "Fast, French support, good for simple queries",
                "latency": "3-4s",
            },
            {
                "key": "t2",
                "name": "Llama2 7B",
                "tier": 2,
                "description": "Deep analysis, code, legal/RGPD, detailed responses",
                "latency": "4-5s",
            },
        ]
    }


@app.get("/api/status")
async def status():
    """Server status."""
    return {
        "status": "healthy",
        "cascade": "T1→T2 (auto-escalate based on query complexity)",
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000, log_level="info")
