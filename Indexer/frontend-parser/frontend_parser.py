#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import uuid
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Iterable, List, Tuple

try:
    from tree_sitter_languages import get_parser
except ImportError as exc:  # pragma: no cover - import guard
    raise ImportError(
        "tree-sitter-languages não está instalado. "
        "Rode `mamba env update -f environment.yml` ou `pip install tree-sitter tree-sitter-languages`."
    ) from exc

TS_PARSER = get_parser("typescript")


@dataclass
class MethodInfo:
    name: str
    signature: str
    content: str
    doc: str


def clean_jsdoc(raw: str) -> str:
    if not raw:
        return ""

    lines: List[str] = []
    for line in raw.splitlines():
        stripped = line.strip()
        stripped = stripped.lstrip("/").lstrip("*").strip()
        stripped = stripped.removesuffix("*/").rstrip("*").strip()
        if stripped and stripped != "/":
            lines.append(stripped)
    return " ".join(lines).strip()


def node_text(node, source: bytes) -> str:
    return source[node.start_byte : node.end_byte].decode("utf-8")


def find_jsdoc_before(node, source: bytes) -> str:
    search_start = max(0, node.start_byte - 3000)
    prefix = source[search_start : node.start_byte].decode("utf-8")
    match = re.search(r"/\*\*[\s\S]*?\*/\s*$", prefix)
    return clean_jsdoc(match.group(0)) if match else ""


def parse_component_metadata_text(text: str) -> Dict[str, Any]:
    meta: Dict[str, Any] = {}
    body_match = re.search(r"@Component\s*\((\{[\s\S]*\})\)", text, re.MULTILINE)
    if not body_match:
        return meta

    body = body_match.group(1)
    selector_match = re.search(r"selector\s*:\s*['\"]([^'\"]+)['\"]", body)
    template_url_match = re.search(r"templateUrl\s*:\s*['\"]([^'\"]+)['\"]", body)
    template_inline_match = re.search(r"template\s*:\s*`([^`]*)`", body, re.MULTILINE)
    style_urls_match = re.search(r"styleUrls\s*:\s*\[([^\]]*)\]", body, re.MULTILINE)

    if selector_match:
        meta["component_selector"] = selector_match.group(1)
    if template_url_match:
        meta["component_template_url"] = template_url_match.group(1)
    if template_inline_match:
        meta["component_inline_template"] = template_inline_match.group(1).strip()
    if style_urls_match:
        raw_urls = style_urls_match.group(1)
        urls = [
            entry.strip().strip("'\"")
            for entry in raw_urls.split(",")
            if entry.strip().strip("'\"")
        ]
        if urls:
            meta["component_style_urls"] = urls

    return meta


def extract_imports(tree, source_bytes: bytes) -> List[str]:
    imports: List[str] = []
    root = tree.root_node
    for child in root.children:
        if child.type == "import_statement":
            imports.append(node_text(child, source_bytes).strip())
    return imports


def extract_component_classes(tree, source_bytes: bytes) -> List[Tuple[str, str, Dict[str, Any], List[MethodInfo]]]:
    """
    Retorna lista de tuplas com (class_name, class_doc, component_metadata, methods).
    """
    root = tree.root_node

    results: List[Tuple[str, str, Dict[str, Any], List[MethodInfo]]] = []

    def walk(node):
        if node.type == "class_declaration":
            class_name_node = node.child_by_field_name("name")
            if not class_name_node:
                return

            decorators = [
                child for child in node.children if child.type == "decorator"
            ]
            component_meta: Dict[str, Any] = {}
            for deco in decorators:
                deco_text = node_text(deco, source_bytes)
                if deco_text.lstrip().startswith("@Component"):
                    component_meta = parse_component_metadata_text(deco_text)

            class_doc = find_jsdoc_before(node, source_bytes)
            class_name = node_text(class_name_node, source_bytes)
            body = node.child_by_field_name("body")
            method_infos: List[MethodInfo] = []

            if body:
                for child in body.children:
                    if child.type == "method_definition":
                        name_node = child.child_by_field_name("name")
                        body_node = child.child_by_field_name("body")
                        if not name_node or not body_node:
                            continue

                        method_name = node_text(name_node, source_bytes)
                        signature_text = source_bytes[
                            child.start_byte : body_node.start_byte
                        ].decode("utf-8")
                        content_text = node_text(child, source_bytes).strip()
                        doc = find_jsdoc_before(child, source_bytes)

                        method_infos.append(
                            MethodInfo(
                                name=method_name,
                                signature=" ".join(signature_text.split()),
                                content=content_text,
                                doc=doc,
                            )
                        )

            results.append((class_name, class_doc, component_meta, method_infos))
        for child in node.children:
            walk(child)

    walk(root)
    return results


def build_document_id(
    parser_name: str, full_context: str, signature: str, source_name: str
) -> str:
    stable_key = f"{parser_name}:{full_context}:{signature}:{source_name}"
    return str(uuid.uuid5(uuid.NAMESPACE_URL, stable_key))


def build_embedding_text(
    class_docs: str,
    method_docs: str,
    signature: str,
    content: str,
) -> str:
    sections = [
        ("Class doc", class_docs),
        ("Method doc", method_docs),
        ("Signature", signature),
        ("Code", content),
    ]

    formatted = []
    for title, value in sections:
        if value:
            formatted.append(f"{title}:\n{value}".strip())
    return "\n\n".join(formatted)


def sanitize_filename(value: str) -> str:
    invalid_chars = '<>:"/\\|?*\n\r\t'
    sanitized = "".join("_" if ch in invalid_chars else ch for ch in value)
    return sanitized.replace(" ", "_")[:200]


def ensure_data_directory(start: Path) -> Path:
    current = start
    while True:
        candidate = current / "data"
        if candidate.exists():
            return candidate
        if current.parent == current:
            break
        current = current.parent

    fallback = start / "data"
    fallback.mkdir(parents=True, exist_ok=True)
    return fallback


def derive_namespace(file_path: Path, repo_root: Path) -> str | None:
    try:
        relative = file_path.resolve().relative_to(repo_root)
    except ValueError:
        return None

    parent_parts = list(relative.parent.parts)
    return ".".join(parent_parts) if parent_parts else None


def save_documents(
    documents: Iterable[Dict[str, Any]], output_dir: Path
) -> List[Path]:
    saved_paths: List[Path] = []
    output_dir.mkdir(parents=True, exist_ok=True)

    for document in documents:
        base_name = document.get("full_context") or document.get("source_name", "item")
        file_path = output_dir / f"{sanitize_filename(base_name)}__{document['id']}.json"
        with file_path.open("w", encoding="utf-8") as fp:
            json.dump(document, fp, indent=2, ensure_ascii=False)
        saved_paths.append(file_path)

    return saved_paths


def build_documents_for_component(
    component_path: Path, parser_name: str
) -> List[Dict[str, Any]]:
    raw_text = component_path.read_text(encoding="utf-8")
    source_bytes = raw_text.encode("utf-8")
    tree = TS_PARSER.parse(source_bytes)
    classes = extract_component_classes(tree, source_bytes)
    imports = extract_imports(tree, source_bytes)
    if not classes:
        raise ValueError("Nenhum componente Angular com @Component foi encontrado.")

    repo_root = find_repo_root(component_path)
    namespace = derive_namespace(component_path, repo_root)

    source_name = component_path.name
    source_path = str(component_path.resolve())

    documents: List[Dict[str, Any]] = []
    for class_name, class_doc, component_meta, methods in classes:
        if not methods:
            continue

        for method in methods:
            full_context = ".".join(
                part for part in [namespace, class_name, method.name] if part
            )
            doc_id = build_document_id(
                parser_name, full_context, method.signature, source_name
            )

            document = {
                "id": doc_id,
                "parser": parser_name,
                "source_name": source_name,
                "source_path": source_path,
                "namespace": namespace,
                "class_name": class_name,
                "method_name": method.name,
                "signature": method.signature,
                "full_context": full_context,
                "content": method.content,
                "method_docs": method.doc,
                "class_docs": class_doc,
                "constants_in_scope": [],
                "readonly_fields_in_scope": [],
                "imports": imports,
                "embedding_text": build_embedding_text(
                    class_doc, method.doc, method.signature, method.content
                ),
                "metadata": dict(component_meta),
            }

            documents.append(document)

    return documents


def find_repo_root(start: Path) -> Path:
    current = start.resolve()
    while True:
        if (current / ".git").exists():
            return current
        if current.parent == current:
            return start.resolve()
        current = current.parent


def main(argv: List[str] | None = None) -> None:
    parser = argparse.ArgumentParser(
        description="Gera metadados de métodos a partir de um componente Angular."
    )
    parser.add_argument(
        "component",
        help="Caminho do arquivo .ts do componente Angular (ex.: app.component.ts)",
    )
    parser.add_argument(
        "--parser-name",
        default="frontend-parser",
        help="Nome do parser usado no JSON (default: frontend-parser).",
    )
    parser.add_argument(
        "--output-dir",
        help="Destino opcional para salvar os JSONs. Por padrão usa data/02-normalization/<parser-name>.",
    )

    args = parser.parse_args(argv)

    component_path = Path(args.component).expanduser().resolve()
    if not component_path.exists():
        raise SystemExit(f"Arquivo não encontrado: {component_path}")

    data_root = ensure_data_directory(component_path.parent)
    # Para alinhar com o fluxo do Roslyn, a saída padrão fica em data/01-parser/<parser-name>
    default_output = data_root / "01-parser" / args.parser_name
    output_dir = Path(args.output_dir).expanduser().resolve() if args.output_dir else default_output

    documents = build_documents_for_component(component_path, parser_name=args.parser_name)
    saved_paths = save_documents(documents, output_dir=output_dir)

    print(f"Gerados {len(saved_paths)} arquivos em {output_dir}")
    for path in saved_paths:
        print(f"  - {path}")


if __name__ == "__main__":
    main()
