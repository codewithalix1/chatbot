from ai.rag import index_knowledge, search_knowledge


# Add knowledge to Pinecone
result = index_knowledge()
print(result)


# Test semantic search
results = search_knowledge(
    "What information can I change for a user?"
)

print("\n--- SEARCH RESULTS ---")

for doc in results:
    print("\nTitle:", doc.metadata.get("title"))
    print("Content:", doc.page_content)