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
            "Had a detailed discussion with Prof. Hegde about possible research directions. "
            "We explored using Retrieval-Augmented Generation (RAG) in autonomous systems and integrating it with place recognition models. "
            "I left the meeting with a list of papers to review and a follow-up scheduled for next week."
        ),
        "timestamp": "2025-03-10T10:00:00Z"
    },
    {
        "text": (
            "Fixed a critical memory leak in the object detection module. "
            "The issue was traced back to a Tensor allocation that wasn’t cleared after inference. "
            "I documented the solution and pushed the patch to the main branch after verifying with unit tests."
        ),
        "timestamp": "2025-03-12T14:00:00Z"
    },
    {
        "text": (
            "Met with the GISA team to finalize plans for the Bollywood Night event. "
            "We secured the venue, confirmed catering, and created a promotion plan using social media and email newsletters. "
            "I volunteered to coordinate logistics on the day of the event and handle the music setup."
        ),
        "timestamp": "2025-03-15T16:00:00Z"
    },
    {
        "text": (
            "Debugged an issue in the LangGraph pipeline for the MCP server. "
            "The agent flow was getting stuck in a loop between the Senior and Tester agents due to incomplete response handling. "
            "I introduced a guard condition to break the cycle and tested with simulated GitHub PRs."
        ),
        "timestamp": "2025-03-20T11:30:00Z"
    },
    {
        "text": (
            "Refactored the RAG retriever logic used in the robotics navigation stack. "
            "I integrated Qdrant as the vector store, added support for ClearML experiment tracking, and optimized the prompt routing logic. "
            "The updated retriever showed improved performance in both simulated and real-world corridor navigation scenarios."
        ),
        "timestamp": "2025-03-25T09:00:00Z"
    },
    {
    "text": (
        "Worked on optimizing the bird sound generation model for our machine learning course project. "
        "I replaced the baseline GAN with a conditional GAN to better control species-specific output. "
        "The generated samples were evaluated using spectrogram comparison and showed improved clarity over the original baseline."
    ),
    "timestamp": "2025-03-27T17:00:00Z"
    },
    {
        "text": (
            "Assisted a teammate in configuring Docker containers for our LangGraph-based agent system. "
            "We faced an issue where inter-agent communication failed due to mismatched network aliases. "
            "After debugging with `docker inspect`, we resolved it by explicitly setting container networks and hostnames."
        ),
        "timestamp": "2025-03-28T13:45:00Z"
    },
    {
        "text": (
            "Had a follow-up meeting with the NYU Information Visualization team. "
            "Presented insights on car color trends in the U.S., showcasing how regional preferences have shifted over time. "
            "I used Altair to build a radial chart that clearly highlighted seasonal and geographic patterns."
        ),
        "timestamp": "2025-03-29T11:00:00Z"
    },
    {
        "text": (
            "Submitted my application for a leadership position in GISA. "
            "I highlighted my past event contributions, including Garba Night and Diwali celebrations, and proposed ideas to improve cross-cultural engagement. "
            "Looking forward to building stronger community ties through tech-integrated planning and feedback collection tools."
        ),
        "timestamp": "2025-03-30T18:00:00Z"
    },
    {
        "text": (
            "Integrated a feedback loop into our RAG + LangGraph pipeline for handling GitHub pull requests. "
            "The tester agent can now provide reject reasons, which are passed back to the coder agent for correction. "
            "This improvement helped close PRs faster and simulate a more realistic multi-agent engineering workflow."
        ),
        "timestamp": "2025-03-31T09:30:00Z"
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
