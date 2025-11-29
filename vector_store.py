from sentence_transformers import SentenceTransformer
import faiss
import glob
import os
from typing import List, Tuple


def read_docs(doc_dir: str):
    paths = sorted(glob.glob(os.path.join(doc_dir, "*.txt")))
    docs = []
    for p in paths:
        with open(p, "r", encoding="utf-8") as f:
            docs.append((os.path.basename(p), f.read().strip()))
    return docs


def chunk_text(text: str, chunk_size=180, overlap=30):
    words = text.split()
    chunks = []
    start = 0

    while start < len(words):
        end = min(start + chunk_size, len(words))
        chunks.append(" ".join(words[start:end]))
        if end == len(words):
            break
        start = max(0, end - overlap)

    return chunks


class VectorStore:
    def __init__(self, embed_model="sentence-transformers/all-MiniLM-L6-v2"):
        self.embedder = SentenceTransformer(embed_model)
        self.corpus = []
        self.meta = []
        self.index = None

    def build(self, docs):
        self.corpus = []
        self.meta = []

        for name, content in docs:
            for i, ch in enumerate(chunk_text(content)):
                self.corpus.append(ch)
                self.meta.append((name, i))

        if not self.corpus:
            return

        enc = self.embedder.encode(
            self.corpus,
            convert_to_numpy=True,
            normalize_embeddings=True
        )
        dim = enc.shape[1]
        self.index = faiss.IndexFlatIP(dim)
        self.index.add(enc)

    def search(self, query, top_k=4):
        if self.index is None:
            return []

        q = self.embedder.encode(
            [query],
            convert_to_numpy=True,
            normalize_embeddings=True
        )

        D, I = self.index.search(q, top_k)

        out = []
        for rank, (score, idx) in enumerate(zip(D[0].tolist(), I[0].tolist()), start=1):
            if idx == -1:
                continue

            out.append({
                "rank": rank,
                "score": float(score),
                "text": self.corpus[idx],
                "doc": self.meta[idx][0],
                "chunk_id": self.meta[idx][1]
            })

        return out
