# ai_client.py

import os
import requests
import time

class AIClient:
    def __init__(self):
        self.api_key = os.getenv("GOOGLE_API_KEY")
        if not self.api_key:
            raise ValueError("Missing GOOGLE_API_KEY in environment")

        # For generation using your Generative Language API (v1beta generateContent)
        # Default generation model (stable)
        self.gen_model = os.getenv("GEN_MODEL", "models/gemini-flash-latest")
        self.gen_url = f"https://generativelanguage.googleapis.com/v1beta/{self.gen_model}:generateContent"

        # Embedding model (from your model list)
        self.embed_model = os.getenv("EMBED_MODEL", "models/text-embedding-004")
        self.embed_url = f"https://generativelanguage.googleapis.com/v1beta/{self.embed_model}:embedText"

        # Note: some deployments use :embedText, :embedContent or :embed - adjust if necessary

    def generate_text(self, prompt: str, model_url: str = None, timeout=60) -> str:
        url = model_url or self.gen_url
        payload = {"contents": [{"parts": [{"text": prompt}]}]}
        headers = {"Content-Type": "application/json"}

        # simple retry/backoff
        backoff = 1
        for attempt in range(4):
            resp = requests.post(f"{url}?key={self.api_key}", json=payload, headers=headers, timeout=timeout)
            if resp.status_code == 200:
                data = resp.json()
                # defensive access
                try:
                    return data["candidates"][0]["content"]["parts"][0]["text"]
                except Exception:
                    return str(data)
            else:
                # print raw for debugging
                print("GEN ERROR:", resp.status_code, resp.text)
                if resp.status_code in (503, 429):
                    time.sleep(backoff)
                    backoff *= 2
                    continue
                raise Exception(f"Generation failed: {resp.status_code} {resp.text}")
        raise Exception("Generation retries exhausted")

    def embed_text(self, texts, timeout=60):
        """
        Accepts a single string or list of strings.
        Supports Gemini embedding endpoints that expect:
        - {"text": "..."} for single input
        - {"texts": ["...", "..."]} for batch
        """
        single = False
        if isinstance(texts, str):
            texts = [texts]
            single = True

        # Google Gemini embedding format
        # Most Gemini endpoints use "texts": [...]
        payload = {"texts": texts}

        headers = {"Content-Type": "application/json"}

        resp = requests.post(
            f"{self.embed_url}?key={self.api_key}",
            json=payload,
            headers=headers,
            timeout=timeout
        )

        if resp.status_code != 200:
            print("EMBED ERROR:", resp.status_code, resp.text)
            raise Exception(f"Embedding failed: {resp.status_code} {resp.text}")

        data = resp.json()

        # Supported response formats
        if "embeddings" in data:
            # Standard Gemini response
            vectors = [e["values"] if "values" in e else e["embedding"] for e in data["embeddings"]]

        elif "data" in data:
            vectors = [x["embedding"] for x in data["data"]]

        else:
            raise Exception(f"Unknown embedding response format: {data}")

        return vectors[0] if single else vectors

