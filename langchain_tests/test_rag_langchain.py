import os
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_ollama import ChatOllama

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DOC_DIR = os.path.join(BASE_DIR, "..", "data", "docs")
DOC_DIR = os.path.abspath(DOC_DIR)

# 1. Read ALL .txt documents from /docs
def load_all_docs(doc_dir):
    texts = []
    for fname in os.listdir(doc_dir):
        if fname.endswith(".txt"):
            path = os.path.join(doc_dir, fname)
            with open(path, "r", encoding="utf-8") as f:
                text = f.read().strip()
                if text:
                    texts.append((fname, text))
    return texts


# 2. Load and chunk documents
def build_chunks(documents):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=300,
        chunk_overlap=30
    )
    chunks = []
    metadata = []

    for fname, text in documents:
        parts = splitter.split_text(text)
        for i, chunk in enumerate(parts):
            chunks.append(chunk)
            metadata.append({"source": fname, "chunk_id": i})
    return chunks, metadata


# 3. Build FAISS vector store
def build_vector_store(chunks, metadata):
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )
    db = FAISS.from_texts(chunks, embeddings, metadatas=metadata)
    return db


# ---------------- MAIN ---------------- #

# Load docs
documents = load_all_docs(DOC_DIR)
print(f"Loaded {len(documents)} documents from /docs")

# Chunk
chunks, metadata = build_chunks(documents)
print(f"Created {len(chunks)} total chunks")

# Build FAISS
db = build_vector_store(chunks, metadata)
retriever = db.as_retriever()

# Ollama LLM
llm = ChatOllama(model="gemma3:4b", base_url="http://localhost:11434")

# -------- TEST QUERY -------- #

while True:
    query = input("\nAsk something (or 'exit'): ")
    if query.lower() == "exit":
        break

    docs = retriever.invoke(query)
    context = "\n\n".join([
        f"[{d.metadata['source']} #{d.metadata['chunk_id']}]\n{d.page_content}"
        for d in docs
    ])

    prompt = f"""
Use ONLY this context to answer the question.

CONTEXT:
{context}

QUESTION:
{query}

Answer:
"""

    ans = llm.invoke(prompt)
    print("\nAI:", ans.content)
