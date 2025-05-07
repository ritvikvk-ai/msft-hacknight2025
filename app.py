import streamlit as st
import weaviate
from sentence_transformers import SentenceTransformer

# Page title and description
st.title("MemoryVault: Time-Aware Semantic Search")
st.markdown("Search across your recent memory entries using semantic similarity.")

# Initialize model and client
model = SentenceTransformer("all-MiniLM-L6-v2")
client = weaviate.Client("http://localhost:8080")

# Input field
query = st.text_input("Enter your query")

# Semantic search
if query:
    vector = model.encode(query).tolist()
    response = client.query.get("MemoryEntry", ["text", "timestamp"]) \
        .with_near_vector({"vector": vector}) \
        .with_limit(3) \
        .do()

    st.subheader("Top Matching Results")
    for item in response["data"]["Get"]["MemoryEntry"]:
        st.markdown(f"**Timestamp:** {item['timestamp']}")
        st.markdown(f"**Text:** {item['text']}")
        st.markdown("---")
