from typing import Any, Dict, List, Optional

import chromadb
from chromadb.api.types import Documents, EmbeddingFunction, Metadatas
from chromadb.utils import embedding_functions

from .. import config
from ..domain.models import DocumentHit, QueryInput, QueryResult
from ..domain.repositories import VectorRepository

import logging
logger = logging.getLogger(__name__)



def build_embedding_function(model_name: str | None = None) -> EmbeddingFunction:
    name = model_name or config.EMBEDDING_MODEL_NAME
    return embedding_functions.SentenceTransformerEmbeddingFunction(model_name=name)


class ChromaVectorRepository(VectorRepository):
    def __init__(
        self,
        db_path: Optional[str] = None,
        collection_name: Optional[str] = None,
        embedding_fn: Optional[EmbeddingFunction] = None,
    ) -> None:
        self.db_path = db_path or str(config.CHROMA_DB_DIR)
        logger.info("Chroma DB path: %s", self.db_path)
        self.collection_name = collection_name or config.CHROMA_COLLECTION
        self.embedding_fn = embedding_fn or build_embedding_function()

        self.client = chromadb.PersistentClient(path=self.db_path)
        self.collection = self.client.get_or_create_collection(
            name=self.collection_name,
            embedding_function=self.embedding_fn,
        )

    def query(self, query: QueryInput) -> QueryResult:
        where = query.filters() or None
        response = self.collection.query(
            query_texts=[query.text],
            n_results=query.top_k,
            where=where,
        )

        hits = _parse_hits(response)
        return QueryResult(query=query.text, hits=hits)


def _parse_hits(response: Dict[str, Any]) -> List[DocumentHit]:
    docs: List[Documents] = response.get("documents") or []
    metas: List[Metadatas] = response.get("metadatas") or []
    ids: List[List[str]] = response.get("ids") or []
    distances: List[List[float]] = response.get("distances") or []

    results: List[DocumentHit] = []
    if not docs:
        return results

    for idx, doc in enumerate(docs[0]):
        meta = metas[0][idx] if metas and metas[0] else {}
        item_id = ids[0][idx] if ids and ids[0] else f"{idx}"
        distance = distances[0][idx] if distances and distances[0] else 0.0
        score = 1 - distance
        results.append(
            DocumentHit(
                id=item_id,
                score=score,
                text=doc,
                metadata=meta,
            )
        )
    return results

