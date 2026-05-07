from __future__ import annotations

from pathlib import Path
from typing import List


class LocalRAG:
    """Minimal local-first RAG wrapper around ChromaDB + sentence-transformers."""

    def __init__(self, persist_directory: Path | str = "knowledge/chroma", collection_name: str = "project_catalyst"):
        self.persist_directory = Path(persist_directory)
        self.persist_directory.mkdir(parents=True, exist_ok=True)
        self.collection_name = collection_name
        self._collection = None
        self._encoder = None

    def _lazy_init(self) -> None:
        if self._collection is not None:
            return
        import chromadb
        from sentence_transformers import SentenceTransformer

        client = chromadb.PersistentClient(path=str(self.persist_directory))
        self._collection = client.get_or_create_collection(self.collection_name)
        self._encoder = SentenceTransformer("all-MiniLM-L6-v2")

    def add_documents(self, paths: List[Path | str]) -> int:
        self._lazy_init()
        texts: List[str] = []
        ids: List[str] = []
        for idx, raw_path in enumerate(paths):
            path = Path(raw_path)
            text = path.read_text(encoding="utf-8")
            texts.append(text)
            ids.append(f"doc-{idx}-{path.name}")

        embeddings = self._encoder.encode(texts).tolist()
        self._collection.add(documents=texts, ids=ids, embeddings=embeddings)
        return len(texts)

    def query(self, text: str, top_k: int = 3) -> List[str]:
        self._lazy_init()
        embedding = self._encoder.encode([text]).tolist()[0]
        result = self._collection.query(query_embeddings=[embedding], n_results=top_k)
        return result.get("documents", [[]])[0]
