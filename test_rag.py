from vector_store import VectorStore, read_docs

print("Reading from docs/...")

docs = read_docs("data/docs")
print("DOC LIST:", docs)

vs = VectorStore()
vs.build(docs)

print("\nSearching for: 'rag'")
results = vs.search("rag")
print("SEARCH RESULTS:", results)
