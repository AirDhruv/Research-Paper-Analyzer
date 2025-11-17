import os
import requests


class AIClient:
    def __init__(self):
        self.api_key = os.getenv("GOOGLE_API_KEY")
        if not self.api_key:
            raise ValueError("GOOGLE_API_KEY not found in .env")

        # ✔ Correct and fully supported model for your key
        self.model = "models/gemini-pro-latest"

        # ✔ Correct REST API endpoint for Generative Language API
        self.url = f"https://generativelanguage.googleapis.com/v1beta/{self.model}:generateContent"

    def summarize(self, prompt: str) -> str:
        payload = {
            "contents": [
                {
                    "parts": [{"text": prompt}]
                }
            ]
        }

        response = requests.post(
            f"{self.url}?key={self.api_key}",
            json=payload,
            headers={"Content-Type": "application/json"}
        )

        if response.status_code != 200:
            print("\n--- GEMINI RAW ERROR ---")
            print(response.text)
            print("--------------------------\n")
            raise Exception("Gemini API Error — see logs above.")

        data = response.json()

        return data["candidates"][0]["content"]["parts"][0]["text"]
