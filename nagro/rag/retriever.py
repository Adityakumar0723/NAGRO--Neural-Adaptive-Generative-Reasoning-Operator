"""
NAGRO 4.1 — Self-Built Retriever for RAG.

Chunks documents, generates embeddings locally, and retrieves relevant context.
"""

from __future__ import annotations
import hashlib
import re

from nagro.rag.vector_store import VectorStore


class Retriever:
    """
    Self-built retrieval system. Chunks text, generates embeddings
    using a local model, and retrieves relevant context for queries.
    """

    def __init__(self, store_path: str = "data/vector_store"):
        self.store = VectorStore(store_path)
        self._embedder = None

    def _get_embedder(self):
        """Lazy-load the local embedding model."""
        if self._embedder is not None:
            return self._embedder

        try:
            from transformers import AutoTokenizer, AutoModel
            import torch

            model_name = "sentence-transformers/all-MiniLM-L6-v2"
            self._tokenizer = AutoTokenizer.from_pretrained(model_name)
            self._embed_model = AutoModel.from_pretrained(model_name)
            self._embed_model.eval()
            self._embedder = True
            return self._embedder
        except ImportError:
            self._embedder = False
            return False

    def _embed_text(self, text: str) -> list[float]:
        """Generate embedding for text using local model."""
        if not self._get_embedder():
            return self._simple_embed(text)

        import torch
        inputs = self._tokenizer(
            text, return_tensors="pt", truncation=True, max_length=512, padding=True
        )
        with torch.no_grad():
            outputs = self._embed_model(**inputs)
        # Mean pooling
        attention_mask = inputs["attention_mask"]
        token_embeddings = outputs.last_hidden_state
        input_mask_expanded = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
        embedding = torch.sum(token_embeddings * input_mask_expanded, 1) / torch.clamp(
            input_mask_expanded.sum(1), min=1e-9
        )
        return embedding[0].tolist()

    def _simple_embed(self, text: str) -> list[float]:
        """Fallback: simple bag-of-words embedding when no model available."""
        words = re.findall(r'\w+', text.lower())
        vocab_size = 384  # Match MiniLM dimension
        embedding = [0.0] * vocab_size
        for word in words:
            idx = int(hashlib.md5(word.encode()).hexdigest(), 16) % vocab_size
            embedding[idx] += 1.0
        # Normalize
        norm = max(sum(x * x for x in embedding) ** 0.5, 1e-9)
        return [x / norm for x in embedding]

    def chunk_text(self, text: str, chunk_size: int = 500, overlap: int = 50) -> list[str]:
        """Split text into overlapping chunks."""
        words = text.split()
        chunks = []
        for i in range(0, len(words), chunk_size - overlap):
            chunk = " ".join(words[i:i + chunk_size])
            if chunk.strip():
                chunks.append(chunk)
        return chunks

    def ingest(self, doc_id: str, text: str, metadata: dict | None = None):
        """Ingest a document: chunk it, embed chunks, store them."""
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
        """Retrieve most relevant document chunks for a query."""
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
        """Retrieve and format context for the LLM."""
        results = self.retrieve(query, top_k=top_k)
        if not results:
            return ""
        context_parts = []
        for i, r in enumerate(results, 1):
            context_parts.append(f"[Source {i}] (relevance: {r['score']})\n{r['content']}")
        return "\n\n---\n\n".join(context_parts)
