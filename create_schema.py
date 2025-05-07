import weaviate

client = weaviate.Client("http://localhost:8080")

class_obj = {
    "class": "MemoryEntry",
    "vectorizer": "none",  # Still using sentence-transformers
    "moduleConfig": {
        "text2vec-transformers": {
            "vectorizeClassName": False
        },
        "bm25": {}  # Enable keyword search
    },
    "properties": [
        {"name": "text", "dataType": ["text"], "moduleConfig": {"bm25": {}}},
        {"name": "timestamp", "dataType": ["date"]}
    ]
}

if "MemoryEntry" in [cls["class"] for cls in client.schema.get()["classes"]]:
    client.schema.delete_class("MemoryEntry")

client.schema.create_class(class_obj)
print("Schema updated for hybrid search.")
