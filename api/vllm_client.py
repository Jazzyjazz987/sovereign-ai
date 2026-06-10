#!/usr/bin/env python3
"""
vLLM client for T3+ inference
Supports OpenAI-compatible API
"""
import requests
import logging
from typing import Optional

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class VLLMClient:
    """Client for vLLM-based inference (T3, T4)."""

    MODELS = {
        "t3": {
            "name": "mistral-7b-instruct",
            "display": "T3 - Mistral 7B (vLLM)",
            "description": "Code, PowerShell, Graph API",
            "latency": "5-8s",
            "url": "http://localhost:8001"
        },
        "t4": {
            "name": "mistral-small-22b",
            "display": "T4 - Mistral Small 22B (vLLM)",
            "description": "Legal, RGPD, administratif",
            "latency": "6-9s",
            "url": "http://localhost:8002"
        }
    }

    def __init__(self, tier: str = "t3"):
        """Initialize vLLM client for specific tier."""
        if tier not in self.MODELS:
            raise ValueError(f"Unknown tier: {tier}")

        self.tier = tier
        self.config = self.MODELS[tier]
        self.base_url = self.config["url"]
        self.model_name = self.config["name"]
        self._verify_connection()

    def _verify_connection(self):
        """Verify connection to vLLM server."""
        try:
            response = requests.get(
                f"{self.base_url}/v1/models",
                timeout=5
            )
            if response.status_code == 200:
                logger.info(f"✅ Connected to {self.config['display']}")
            else:
                logger.warning(f"⚠️ vLLM server returned {response.status_code}")
        except Exception as e:
            logger.warning(f"⚠️ Could not connect to {self.base_url}: {e}")

    def query(self, prompt: str, system: Optional[str] = None) -> str:
        """Query vLLM model."""
        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})

        try:
            logger.info(f"🔀 Querying {self.tier.upper()} ({self.model_name})...")
            response = requests.post(
                f"{self.base_url}/v1/chat/completions",
                json={
                    "model": self.model_name,
                    "messages": messages,
                    "temperature": 0.7,
                    "max_tokens": 2048,
                    "stream": False
                },
                timeout=300
            )

            if response.status_code != 200:
                raise Exception(f"API error: {response.status_code}")

            result = response.json()["choices"][0]["message"]["content"]
            logger.info("✅ Response received")
            return result

        except requests.exceptions.Timeout:
            logger.error("❌ Request timeout")
            raise
        except Exception as e:
            logger.error(f"❌ Error: {str(e)}")
            raise

    def query_stream(self, prompt: str, system: Optional[str] = None):
        """Stream response from vLLM."""
        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})

        try:
            logger.info(f"🔀 Streaming from {self.tier.upper()}...")
            response = requests.post(
                f"{self.base_url}/v1/chat/completions",
                json={
                    "model": self.model_name,
                    "messages": messages,
                    "temperature": 0.7,
                    "max_tokens": 2048,
                    "stream": True
                },
                timeout=300,
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
                                chunk = __import__('json').loads(data)
                                content = chunk['choices'][0]['delta'].get('content', '')
                                if content:
                                    yield content
                    except:
                        pass

            logger.info("✅ Stream complete")

        except Exception as e:
            logger.error(f"❌ Streaming error: {str(e)}")
            raise


if __name__ == "__main__":
    # Test T3
    try:
        client = VLLMClient("t3")
        response = client.query("Écris une fonction Python pour valider un email")
        print("\n=== Response ===")
        print(response)
    except Exception as e:
        print(f"Error: {e}")
