import weaviate

client = weaviate.Client("http://localhost:8080")

query = "projects"

response = client.query.get("MemoryEntry", ["text", "timestamp"]) \
    .with_bm25(query=query) \
    .with_limit(5) \
    .do()

results = response.get("data", {}).get("Get", {}).get("MemoryEntry", [])

if not results:
    print("\nNo results found with BM25.")
else:
    print("\nBM25 Results:\n")
    for item in results:
        print(f"Timestamp: {item['timestamp']}")
        print(f"Text: {item['text']}\n")
