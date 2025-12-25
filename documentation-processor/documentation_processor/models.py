from pathlib import Path
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class ParserRecord(BaseModel):
    parser_name: str
    source_path: Path
    payload: Dict[str, Any]

    class Config:
        arbitrary_types_allowed = True


class NormalizedDocument(BaseModel):
    id: str
    parser: str
    source_name: str
    source_path: str
    namespace: Optional[str] = None
    class_name: Optional[str] = None
    method_name: Optional[str] = None
    signature: Optional[str] = None
    full_context: str
    content: str
    method_docs: Optional[str] = None
    class_docs: Optional[str] = None
    constants_in_scope: List[str] = Field(default_factory=list)
    readonly_fields_in_scope: List[str] = Field(default_factory=list)
    imports: List[str] = Field(default_factory=list)
    embedding_text: str
    metadata: Dict[str, Any] = Field(default_factory=dict)

    def chroma_metadata(self) -> Dict[str, Any]:
        meta: Dict[str, Any] = {
            "parser": self.parser,
            "namespace": self.namespace,
            "class_name": self.class_name,
            "method_name": self.method_name,
            "signature": self.signature,
            "full_context": self.full_context,
            "source_name": self.source_name,
            "source_path": self.source_path,
        }

        constants = "\n".join(self.constants_in_scope) if self.constants_in_scope else None
        readonlys = (
            "\n".join(self.readonly_fields_in_scope)
            if self.readonly_fields_in_scope
            else None
        )
        imports = "\n".join(self.imports) if self.imports else None
        if constants:
            meta["constants_in_scope"] = constants
        if readonlys:
            meta["readonly_fields_in_scope"] = readonlys
        if imports:
            meta["imports"] = imports

        for key, value in self.metadata.items():
            if isinstance(value, (str, int, float, bool)):
                meta[f"extra_{key}"] = value

        return {k: v for k, v in meta.items() if v is not None}
