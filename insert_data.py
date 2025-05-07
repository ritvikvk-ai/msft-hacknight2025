import weaviate
import os
import openai
from datetime import datetime
from time import sleep

# Connect to Weaviate
client = weaviate.Client("http://localhost:8080")

# OPTIONAL: set your OpenAI key as env var
openai.api_key = os.getenv("OPENAI_API_KEY")

# Dummy memories
memories = [
    {
        "text": (
            "Sample text"
        ),
        "timestamp": "2025-03-10T10:00:00Z"
    }
]

# Helper: get embedding
from sentence_transformers import SentenceTransformer

# Load local embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")  # ~384-dim vector

def get_embedding(text):
    return model.encode(text).tolist()

# Upload memories
for memory in memories:
    vector = get_embedding(memory["text"])
    client.data_object.create(
        data_object={
            "text": memory["text"],
            "timestamp": memory["timestamp"]
        },
        class_name="MemoryEntry",
        vector=vector
    )
    print(f"Inserted: {memory['text']}")
    sleep(1)  # Optional throttle
