from __future__ import annotations

import argparse
from typing import List

from . import config
from .normalizer import load_parser_records, normalize_record, save_normalized_documents
from .vector_store import get_collection, upsert_documents


def run_pipeline(collection_name: str | None = None) -> None:
    config.ensure_directories()

    print(f"[1/3] Lendo parsers em: {config.PARSER_INPUT_DIR}")
    records = load_parser_records()
    if not records:
        print("Nenhum arquivo JSON encontrado em data/01-parser/*")
        return

    normalized = [normalize_record(record) for record in records]

    print(f"[2/3] Salvando normalizações em: {config.NORMALIZATION_DIR}")
    saved_paths = save_normalized_documents(normalized)
    for path in saved_paths:
        print(f"  - {path}")

    print(f"[3/3] Inserindo no ChromaDB em: {config.CHROMA_DB_DIR}")
    _, collection = get_collection(collection_name)
    inserted = upsert_documents(normalized, collection)
    print(f"Concluído: {inserted} itens na coleção '{collection.name}'.")


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Normaliza a saída dos parsers e envia para o ChromaDB."
    )
    parser.add_argument(
        "--collection",
        help="Nome da coleção no ChromaDB (padrão: documentation ou CHROMA_COLLECTION).",
        default=None,
    )
    return parser


def main(argv: List[str] | None = None) -> None:
    args = build_arg_parser().parse_args(argv)
    run_pipeline(collection_name=args.collection)


if __name__ == "__main__":
    main()
