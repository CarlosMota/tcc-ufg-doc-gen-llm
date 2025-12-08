import os
from pathlib import Path


def find_repo_root(start_path: Path | None = None) -> Path:
    """Resolve o diretório raiz procurando pela pasta data/."""
    start = start_path or Path(__file__).resolve()
    for candidate in [start, *start.parents]:
        data_dir = candidate / "data"
        if data_dir.exists():
            return candidate
    raise FileNotFoundError("Não foi possível localizar a pasta 'data/'.")


REPO_ROOT = find_repo_root()
DATA_DIR = Path(os.getenv("DATA_DIR", REPO_ROOT / "data")).resolve()
PARSER_INPUT_DIR = Path(os.getenv("PARSER_INPUT_DIR", DATA_DIR / "01-parser")).resolve()
NORMALIZATION_DIR = Path(os.getenv("NORMALIZATION_DIR", DATA_DIR / "02-normalization")).resolve()
CHROMA_DB_DIR = Path(os.getenv("CHROMA_DB_DIR", DATA_DIR / "03-vector-store")).resolve()
DEFAULT_COLLECTION_NAME = os.getenv("CHROMA_COLLECTION", "documentation")


def ensure_directories() -> None:
    """Garante que as pastas de saída existam."""
    NORMALIZATION_DIR.mkdir(parents=True, exist_ok=True)
    CHROMA_DB_DIR.mkdir(parents=True, exist_ok=True)

