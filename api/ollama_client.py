#!/usr/bin/env python3
"""
Ollama client for Sovereign AI Stack (T1/T2 models)
"""
import requests
import logging
import json
from typing import Optional, Dict, Any
from dataclasses import dataclass

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class ModelConfig:
    """Model configuration."""
    name: str
    display_name: str
    description: str
    latency_estimate: str


class OllamaClient:
    """Client for querying Ollama models."""

    MODELS = {
        "t1": ModelConfig(
            name="mistral:7b",
            display_name="T1 - Mistral 7B",
            description="Fast responses, French support",
            latency_estimate="3-4s"
        ),
        "t2": ModelConfig(
            name="llama2:7b",
            display_name="T2 - Llama2 7B",
            description="Deep analysis, detailed responses",
            latency_estimate="4-5s"
        ),
    }

    def __init__(self, base_url: str = "http://localhost:11434", timeout: int = 60):
        """Initialize Ollama client.

        Args:
            base_url: Ollama server URL
            timeout: Request timeout in seconds
        """
        self.base_url = base_url
        self.timeout = timeout
        self._verify_connection()

    def _verify_connection(self):
        """Verify connection to Ollama server."""
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            if response.status_code == 200:
                logger.info("✅ Connected to Ollama server")
                models = response.json().get("models", [])
                logger.info(f"   Available models: {', '.join([m['name'] for m in models])}")
            else:
                raise ConnectionError(f"Ollama returned status {response.status_code}")
        except Exception as e:
            logger.warning(f"⚠️  Could not connect to Ollama: {e}")

    def query(self, model: str, prompt: str, system: Optional[str] = None) -> str:
        """Query a model synchronously.

        Args:
            model: Model key ("t1" or "t2") or full model name
            prompt: User prompt
            system: Optional system message

        Returns:
            Model response
        """
        model_name = self._resolve_model(model)

        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})

        try:
            logger.info(f"🔄 Querying {model_name}...")
            response = requests.post(
                f"{self.base_url}/v1/chat/completions",
                json={
                    "model": model_name,
                    "messages": messages,
                    "stream": False
                },
                timeout=self.timeout
            )

            if response.status_code != 200:
                raise Exception(f"API error: {response.status_code} - {response.text}")

            result = response.json()["choices"][0]["message"]["content"]
            logger.info("✅ Response received")
            return result

        except requests.exceptions.Timeout:
            logger.error("❌ Request timeout - model may be thinking")
            raise
        except Exception as e:
            logger.error(f"❌ Error: {str(e)}")
            raise

    def query_stream(self, model: str, prompt: str, system: Optional[str] = None):
        """Query a model with streaming response.

        Args:
            model: Model key ("t1" or "t2") or full model name
            prompt: User prompt
            system: Optional system message

        Yields:
            Text chunks as they arrive
        """
        model_name = self._resolve_model(model)

        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})

        try:
            logger.info(f"🔄 Streaming from {model_name}...")
            response = requests.post(
                f"{self.base_url}/v1/chat/completions",
                json={
                    "model": model_name,
                    "messages": messages,
                    "stream": True
                },
                timeout=self.timeout,
                stream=True
            )

            if response.status_code != 200:
                raise Exception(f"API error: {response.status_code}")

            for line in response.iter_lines():
                if line:
                    try:
                        if line.startswith(b'data: '):
                            data = line[6:].decode()
                            if data.strip() != '[DONE]':
                                chunk = json.loads(data)['choices'][0]['delta'].get('content', '')
                                if chunk:
                                    yield chunk
                    except (json.JSONDecodeError, KeyError, IndexError):
                        pass

            logger.info("✅ Stream complete")

        except Exception as e:
            logger.error(f"❌ Streaming error: {str(e)}")
            raise

    def batch_query(self, model: str, prompts: list) -> list:
        """Query multiple prompts sequentially.

        Args:
            model: Model key ("t1" or "t2")
            prompts: List of prompts

        Returns:
            List of responses
        """
        results = []
        for i, prompt in enumerate(prompts, 1):
            logger.info(f"Processing {i}/{len(prompts)}...")
            try:
                result = self.query(model, prompt)
                results.append(result)
            except Exception as e:
                logger.error(f"Failed prompt {i}: {e}")
                results.append(None)
        return results

    def get_model_info(self, model: str) -> Dict[str, str]:
        """Get information about a model.

        Args:
            model: Model key ("t1" or "t2")

        Returns:
            Model information dict
        """
        model_key = model.lower() if model.lower() in ["t1", "t2"] else "t1"
        config = self.MODELS[model_key]
        return {
            "key": model_key,
            "name": config.name,
            "display_name": config.display_name,
            "description": config.description,
            "latency": config.latency_estimate
        }

    def _resolve_model(self, model: str) -> str:
        """Convert model key to full model name."""
        model_lower = model.lower()
        if model_lower in self.MODELS:
            return self.MODELS[model_lower].name
        return model  # Assume it's already a full model name


# Example usage
if __name__ == "__main__":
    client = OllamaClient()

    # Simple query
    print("\n=== SIMPLE QUERY ===")
    response = client.query("t1", "Explique RGPD brievement")
    print(response)

    # Streaming query
    print("\n=== STREAMING QUERY ===")
    print("Response: ", end="", flush=True)
    for chunk in client.query_stream("t1", "What is AI?"):
        print(chunk, end="", flush=True)
    print("\n")

    # Batch query
    print("\n=== BATCH QUERY ===")
    prompts = [
        "Bonjour",
        "Qui es-tu ?",
        "Comment ça marche ?"
    ]
    results = client.batch_query("t1", prompts)
    for prompt, result in zip(prompts, results):
        print(f"Q: {prompt}\nA: {result[:100]}...\n")

    # Model info
    print("\n=== MODEL INFO ===")
    print(client.get_model_info("t1"))
    print(client.get_model_info("t2"))
