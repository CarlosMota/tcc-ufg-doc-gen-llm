import json
import uuid
from pathlib import Path
from typing import Iterable, List

from .config import NORMALIZATION_DIR, PARSER_INPUT_DIR, ensure_directories
from .models import NormalizedDocument, ParserRecord


KNOWN_FIELDS = {
    "file_path",
    "namespace",
    "class_name",
    "method_name",
    "signature",
    "content_length",
    "content",
    "method_xml_docs",
    "class_xml_docs",
    "constants_in_scope",
    "readonly_fields_in_scope",
    "full_context",
}


def load_parser_records(parser_root: Path | None = None) -> List[ParserRecord]:
    parser_root = parser_root or PARSER_INPUT_DIR
    records: List[ParserRecord] = []

    for parser_dir in sorted(parser_root.glob("*")):
        if not parser_dir.is_dir():
            continue

        for file_path in sorted(parser_dir.glob("*.json")):
            try:
                raw = json.loads(file_path.read_text(encoding="utf-8"))
            except json.JSONDecodeError as exc:
                raise ValueError(f"Erro ao ler {file_path}: {exc}") from exc

            records.append(
                ParserRecord(
                    parser_name=parser_dir.name,
                    source_path=file_path,
                    payload=raw,
                )
            )

    return records


def normalize_record(record: ParserRecord) -> NormalizedDocument:
    payload = record.payload

    full_context = payload.get("full_context") or _compose_full_context(payload)
    signature = payload.get("signature")
    content = payload.get("content") or ""

    doc_id = _build_document_id(
        parser_name=record.parser_name,
        full_context=full_context,
        signature=signature,
        source_name=record.source_path.name,
    )

    extra_metadata = {k: v for k, v in payload.items() if k not in KNOWN_FIELDS}
    constants = payload.get("constants_in_scope") or []
    readonlys = payload.get("readonly_fields_in_scope") or []

    embedding_text = _build_embedding_text(
        class_xml_docs=payload.get("class_xml_docs") or "",
        method_xml_docs=payload.get("method_xml_docs") or "",
        signature=signature or "",
        content=content,
        constants=constants,
        readonlys=readonlys,
    )

    return NormalizedDocument(
        id=doc_id,
        parser=record.parser_name,
        source_name=record.source_path.name,
        source_path=str(record.source_path),
        namespace=payload.get("namespace"),
        class_name=payload.get("class_name"),
        method_name=payload.get("method_name"),
        signature=signature,
        full_context=full_context,
        content=content,
        method_xml_docs=payload.get("method_xml_docs"),
        class_xml_docs=payload.get("class_xml_docs"),
        constants_in_scope=list(constants),
        readonly_fields_in_scope=list(readonlys),
        embedding_text=embedding_text,
        metadata=extra_metadata,
    )


def save_normalized_documents(
    documents: Iterable[NormalizedDocument],
    output_root: Path | None = None,
) -> list[Path]:
    output_root = output_root or NORMALIZATION_DIR
    ensure_directories()
    saved_paths: list[Path] = []

    for document in documents:
        parser_dir = output_root / document.parser
        parser_dir.mkdir(parents=True, exist_ok=True)

        base_name = document.full_context or document.source_name
        safe_name = _sanitize_filename(base_name)
        file_path = parser_dir / f"{safe_name}__{document.id}.json"

        with file_path.open("w", encoding="utf-8") as fp:
            json.dump(document.dict(), fp, indent=2, ensure_ascii=False)

        saved_paths.append(file_path)

    return saved_paths


def _compose_full_context(payload: dict) -> str:
    namespace = payload.get("namespace")
    class_name = payload.get("class_name")
    method_name = payload.get("method_name")
    pieces = [part for part in [namespace, class_name, method_name] if part]
    return ".".join(pieces) or "unknown_context"


def _build_document_id(
    parser_name: str, full_context: str, signature: str | None, source_name: str
) -> str:
    stable_key = f"{parser_name}:{full_context}:{signature or ''}:{source_name}"
    return str(uuid.uuid5(uuid.NAMESPACE_URL, stable_key))


def _build_embedding_text(
    class_xml_docs: str,
    method_xml_docs: str,
    signature: str,
    content: str,
    constants: list[str],
    readonlys: list[str],
) -> str:
    sections = [
        ("Class doc", class_xml_docs),
        ("Method doc", method_xml_docs),
        ("Signature", signature),
        ("Code", content),
    ]

    if constants:
        sections.append(("Constants", "\n".join(constants)))
    if readonlys:
        sections.append(("Readonly fields", "\n".join(readonlys)))

    formatted = []
    for title, value in sections:
        if value:
            formatted.append(f"{title}:\n{value}".strip())
    return "\n\n".join(formatted)


def _sanitize_filename(value: str) -> str:
    invalid_chars = '<>:"/\\|?*\n\r\t'
    sanitized = "".join("_" if ch in invalid_chars else ch for ch in value)
    return sanitized.replace(" ", "_")[:200]

