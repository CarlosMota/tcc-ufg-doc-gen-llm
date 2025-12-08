import os
from typing import Iterable, Tuple

import chromadb
from chromadb.api import Collection
from chromadb.utils import embedding_functions

from .config import CHROMA_DB_DIR, DEFAULT_COLLECTION_NAME
from .models import NormalizedDocument


def _build_embedding_function():
    """Seleciona a função de embedding (SentenceTransformer por padrão)."""
    model_name = os.getenv("EMBEDDING_MODEL_NAME", "all-MiniLM-L6-v2")
    return embedding_functions.SentenceTransformerEmbeddingFunction(
        model_name=model_name
    )


def get_collection(collection_name: str | None = None) -> Tuple[chromadb.ClientAPI, Collection]:
    collection_name = collection_name or DEFAULT_COLLECTION_NAME
    client = chromadb.PersistentClient(path=str(CHROMA_DB_DIR))
    embedding_fn = _build_embedding_function()
    collection = client.get_or_create_collection(
        name=collection_name,
        embedding_function=embedding_fn,
    )
    return client, collection


def upsert_documents(
    documents: Iterable[NormalizedDocument],
    collection: Collection,
) -> int:
    ids = []
    docs = []
    metadatas = []

    for doc in documents:
        ids.append(doc.id)
        docs.append(doc.embedding_text)
        metadatas.append(doc.chroma_metadata())

    if ids:
        collection.upsert(ids=ids, documents=docs, metadatas=metadatas)

    return len(ids)

