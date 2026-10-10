"""
NAGRO 4.1 — Self-Built Vector Store for RAG.

Simple but effective vector store using numpy for similarity search.
No external vector database needed.
"""

from __future__ import annotations
import json
import math
from pathlib import Path
from dataclasses import dataclass, field


@dataclass
class Document:
    """A document chunk with its embedding."""
    id: str
    content: str
    metadata: dict = field(default_factory=dict)
    embedding: list[float] = field(default_factory=list)


class VectorStore:
    """
    Self-built vector store for RAG. Uses cosine similarity.
    No ChromaDB, no Pinecone, no external dependencies.
    """

    def __init__(self, store_path: str = "data/vector_store"):
        self.store_path = Path(store_path)
        self.store_path.mkdir(parents=True, exist_ok=True)
        self.documents: list[Document] = []
        self._load()

    def _cosine_similarity(self, a: list[float], b: list[float]) -> float:
        """Compute cosine similarity between two vectors."""
        if len(a) != len(b) or not a:
            return 0.0
        dot = sum(x * y for x, y in zip(a, b))
        norm_a = math.sqrt(sum(x * x for x in a))
        norm_b = math.sqrt(sum(x * x for x in b))
        if norm_a == 0 or norm_b == 0:
            return 0.0
        return dot / (norm_a * norm_b)

    def add(self, doc_id: str, content: str, embedding: list[float], metadata: dict | None = None):
        """Add a document to the store."""
        doc = Document(
            id=doc_id,
            content=content,
            embedding=embedding,
            metadata=metadata or {},
        )
        # Replace if exists
        self.documents = [d for d in self.documents if d.id != doc_id]
        self.documents.append(doc)
        self._save()

    def search(self, query_embedding: list[float], top_k: int = 5) -> list[tuple[Document, float]]:
        """Search for most similar documents."""
        if not self.documents:
            return []

        scored = []
        for doc in self.documents:
            if doc.embedding:
                score = self._cosine_similarity(query_embedding, doc.embedding)
                scored.append((doc, score))

        scored.sort(key=lambda x: x[1], reverse=True)
        return scored[:top_k]

    def delete(self, doc_id: str):
        """Remove a document from the store."""
        self.documents = [d for d in self.documents if d.id != doc_id]
        self._save()

    def clear(self):
        """Clear all documents."""
        self.documents = []
        self._save()

    def _save(self):
        """Persist store to disk."""
        data = []
        for doc in self.documents:
            data.append({
                "id": doc.id,
                "content": doc.content,
                "metadata": doc.metadata,
                "embedding": doc.embedding,
            })
        filepath = self.store_path / "store.json"
        filepath.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")

    def _load(self):
        """Load store from disk."""
        filepath = self.store_path / "store.json"
        if not filepath.exists():
            return
        try:
            data = json.loads(filepath.read_text(encoding="utf-8"))
            self.documents = [
                Document(
                    id=d["id"],
                    content=d["content"],
                    metadata=d.get("metadata", {}),
                    embedding=d.get("embedding", []),
                )
                for d in data
            ]
        except (json.JSONDecodeError, KeyError):
            self.documents = []

    @property
    def count(self) -> int:
        return len(self.documents)
