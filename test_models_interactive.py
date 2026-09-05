#!/usr/bin/env python3
import requests
import sys

OLLAMA_URL = "http://localhost:11434"
MODELS = {
    "1": ("mistral:7b", "T1 - Mistral 7B (Fast)"),
    "2": ("llama2:7b", "T2 - Llama2 7B (Deep)"),
}

def query_model(model, prompt, verbose=False):
    """Query a model and return response."""
    try:
        response = requests.post(
            f"{OLLAMA_URL}/v1/chat/completions",
            json={
                "model": model,
                "messages": [{"role": "user", "content": prompt}],
                "stream": False
            },
            timeout=60
        )

        if response.status_code == 200:
            data = response.json()
            return data["choices"][0]["message"]["content"]
        else:
            return f"Error: {response.status_code} - {response.text}"
    except requests.exceptions.Timeout:
        return "Error: Request timeout (model may be thinking)"
    except Exception as e:
        return f"Error: {str(e)}"

def main():
    print("\n" + "="*60)
    print("SOVEREIGN AI STACK - Interactive Model Testing")
    print("="*60)

    while True:
        print("\nSelect model:")
        for key, (model, desc) in MODELS.items():
            print(f"  {key}) {desc}")
        print("  0) Exit")

        choice = input("\nChoice [0-2]: ").strip()

        if choice == "0":
            print("\nExiting...")
            break

        if choice not in MODELS:
            print("Invalid choice")
            continue

        model_name, model_desc = MODELS[choice]
        print(f"\nUsing: {model_desc}")
        print("(Type 'back' to return to model selection, 'exit' to quit)\n")

        while True:
            prompt = input(f">>> ").strip()

            if prompt.lower() == "back":
                break
            if prompt.lower() == "exit":
                print("\nExiting...")
                return
            if not prompt:
                continue

            print(f"\n⏳ Querying {model_name}...\n")
            response = query_model(model_name, prompt)
            print(f"Response:\n{response}\n")
            print("-" * 60)

if __name__ == "__main__":
    main()
