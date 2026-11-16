
import os
from pathlib import Path
from dotenv import load_dotenv
from huggingface_hub import InferenceClient

# Load environment variables
env_path = Path(__file__).resolve().parent / ".env"
load_dotenv(env_path)

HF_TOKEN = os.getenv("HF_Token")

# Initialize InferenceClient
client = InferenceClient(
    # model="mistralai/Mistral-7B-Instruct-v0.3",
    model = "google/gemma-2-2b-it",
    token=HF_TOKEN
)

# Generate response
response = client.chat_completion(
    messages=[
        {
            "role": "user",
            "content": "What is Generative AI?"
        }
    ],
    max_tokens=200
)

print(response.choices[0].message.content)
