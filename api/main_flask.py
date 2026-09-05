#!/usr/bin/env python3
"""
Flask server for Sovereign AI Stack (T1/T2 models via Ollama)
Run: flask run --host 0.0.0.0 --port 5000
Or: python main_flask.py
"""
from flask import Flask, request, jsonify, Response
import logging
from api.ollama_client import OllamaClient

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Initialize client once
try:
    client = OllamaClient()
    logger.info("✅ Flask app initialized with Ollama client")
except Exception as e:
    logger.warning(f"⚠️  Ollama connection warning: {e}")
    client = None


@app.route("/health", methods=["GET"])
def health():
    """Health check endpoint."""
    try:
        if client:
            return jsonify({"status": "healthy", "service": "sovereign-ai-flask-api"})
        return jsonify({"status": "warning", "message": "Ollama not connected"}), 503
    except Exception as e:
        return jsonify({"status": "unhealthy", "error": str(e)}), 503


@app.route("/models", methods=["GET"])
def list_models():
    """List available models."""
    if not client:
        return jsonify({"error": "Ollama client not initialized"}), 503

    models = []
    for key, config in client.MODELS.items():
        models.append({
            "key": key,
            "name": config.name,
            "display_name": config.display_name,
            "description": config.description,
            "latency": config.latency_estimate
        })
    return jsonify({"models": models})


@app.route("/query", methods=["POST"])
def query():
    """Query a model synchronously."""
    if not client:
        return jsonify({"error": "Ollama client not initialized"}), 503

    try:
        data = request.get_json()
        model = data.get("model", "t1")
        prompt = data.get("prompt")
        system = data.get("system")

        if not prompt:
            return jsonify({"error": "Missing prompt"}), 400

        response = client.query(model, prompt, system)
        model_config = client.get_model_info(model)

        return jsonify({
            "model": model_config["display_name"],
            "prompt": prompt,
            "response": response,
            "latency_estimate": model_config["latency"]
        })

    except Exception as e:
        logger.error(f"Query error: {e}")
        return jsonify({"error": str(e)}), 500


@app.route("/query-stream", methods=["POST"])
def query_stream():
    """Query a model with streaming response."""
    if not client:
        return jsonify({"error": "Ollama client not initialized"}), 503

    try:
        data = request.get_json()
        model = data.get("model", "t1")
        prompt = data.get("prompt")
        system = data.get("system")

        if not prompt:
            return jsonify({"error": "Missing prompt"}), 400

        def generate():
            try:
                for chunk in client.query_stream(model, prompt, system):
                    yield chunk

            except Exception as e:
                logger.error(f"Stream error: {e}")
                yield f"Error: {str(e)}"

        return Response(generate(), mimetype="text/event-stream")

    except Exception as e:
        logger.error(f"Stream setup error: {e}")
        return jsonify({"error": str(e)}), 500


@app.route("/batch", methods=["POST"])
def batch_query():
    """Process multiple queries in batch."""
    if not client:
        return jsonify({"error": "Ollama client not initialized"}), 503

    try:
        requests = request.get_json()
        if not isinstance(requests, list):
            return jsonify({"error": "Expected list of queries"}), 400

        results = []
        for req in requests:
            try:
                response = client.query(req.get("model", "t1"), req.get("prompt"), req.get("system"))
                results.append({
                    "prompt": req.get("prompt"),
                    "response": response,
                    "status": "success"
                })
            except Exception as e:
                results.append({
                    "prompt": req.get("prompt"),
                    "error": str(e),
                    "status": "failed"
                })

        return jsonify({
            "results": results,
            "total": len(requests),
            "succeeded": sum(1 for r in results if r["status"] == "success")
        })

    except Exception as e:
        logger.error(f"Batch error: {e}")
        return jsonify({"error": str(e)}), 500


@app.route("/info", methods=["GET"])
def info():
    """API information."""
    return jsonify({
        "name": "Sovereign AI Stack API (Flask)",
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
            "simple": 'curl -X POST http://localhost:5000/query -H "Content-Type: application/json" -d \'{"model":"t1","prompt":"test"}\'',
            "streaming": "Same endpoint, get stream response",
            "batch": "POST /batch with array of queries"
        }
    })


@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "Endpoint not found. Try GET /info for available endpoints"}), 404


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
