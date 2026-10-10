"""
NAGRO 4.1 — Self-Built Retriever for RAG.

Chunks documents and retrieves relevant context using NAGRO's own
TF-IDF based embeddings. No external models needed.
"""

from __future__ import annotations
import hashlib
import re
import math
from collections import Counter

from nagro.rag.vector_store import VectorStore


class Retriever:
    """
    100% self-built retrieval system. Chunks text, generates embeddings
    using NAGRO's own TF-IDF algorithm, and retrieves relevant context.
    No PyTorch. No Transformers. No external models.
    """

    def __init__(self, store_path: str = "data/vector_store"):
        self.store = VectorStore(store_path)

    def _embed_text(self, text: str) -> list[float]:
        """Generate embedding using NAGRO's own TF-IDF based algorithm."""
        words = re.findall(r'\w+', text.lower())
        vocab_size = 384

        word_counts = Counter(words)
        total = len(words) if words else 1
        embedding = [0.0] * vocab_size

        for word, count in word_counts.items():
            tf = count / total
            idf = math.log(1 + 1.0 / (1 + len(word) * 0.1))
            tfidf = tf * idf

            idx = int(hashlib.md5(word.encode()).hexdigest(), 16) % vocab_size
            embedding[idx] += tfidf

            idx2 = int(hashlib.sha1(word.encode()).hexdigest(), 16) % vocab_size
            embedding[idx2] += tfidf * 0.5

        norm = max(sum(x * x for x in embedding) ** 0.5, 1e-9)
        return [x / norm for x in embedding]

    def chunk_text(self, text: str, chunk_size: int = 500, overlap: int = 50) -> list[str]:
        words = text.split()
        chunks = []
        for i in range(0, len(words), chunk_size - overlap):
            chunk = " ".join(words[i:i + chunk_size])
            if chunk.strip():
                chunks.append(chunk)
        return chunks

    def ingest(self, doc_id: str, text: str, metadata: dict | None = None):
        chunks = self.chunk_text(text)
        for i, chunk in enumerate(chunks):
            chunk_id = f"{doc_id}_chunk_{i}"
            embedding = self._embed_text(chunk)
            self.store.add(
                doc_id=chunk_id,
                content=chunk,
                embedding=embedding,
                metadata={**(metadata or {}), "parent_doc": doc_id, "chunk_index": i},
            )

    def retrieve(self, query: str, top_k: int = 3) -> list[dict]:
        query_embedding = self._embed_text(query)
        results = self.store.search(query_embedding, top_k=top_k)
        return [
            {
                "content": doc.content,
                "score": round(score, 4),
                "metadata": doc.metadata,
            }
            for doc, score in results
        ]

    def build_context(self, query: str, top_k: int = 3) -> str:
        results = self.retrieve(query, top_k=top_k)
        if not results:
            return ""
        context_parts = []
        for i, r in enumerate(results, 1):
            context_parts.append(f"[Source {i}] (relevance: {r['score']})\n{r['content']}")
        return "\n\n---\n\n".join(context_parts)
