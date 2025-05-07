import weaviate

client = weaviate.Client("http://localhost:8080")

response = client.query.get("MemoryEntry", ["text", "timestamp"]).with_limit(10).do()

results = response.get("data", {}).get("Get", {}).get("MemoryEntry", [])

if not results:
    print("No data found in Weaviate.")
else:
    print(f"Found {len(results)} entries:")
    for item in results:
        print(f"- {item['timestamp']}: {item['text']}")
