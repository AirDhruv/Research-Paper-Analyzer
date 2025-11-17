import os, requests, json

API_KEY = os.getenv("GOOGLE_API_KEY")

url = "https://generativelanguage.googleapis.com/v1beta/openai/models"

headers = {
    "Authorization": f"Bearer {API_KEY}"
}

res = requests.get(url, headers=headers)

print("\n--- AVAILABLE MODELS ---\n")
print(json.dumps(res.json(), indent=2))
print("\n------------------------\n")
