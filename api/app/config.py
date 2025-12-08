import os
from pathlib import Path


def find_repo_root(start_path: Path | None = None) -> Path:
    start = start_path or Path(__file__).resolve()
    for candidate in [start, *start.parents]:
        if (candidate / "data").exists():
            return candidate
    return Path(__file__).resolve().parent.parent


REPO_ROOT = find_repo_root()
DATA_DIR = Path(os.getenv("DATA_DIR", REPO_ROOT / "data")).resolve()
CHROMA_DB_DIR = Path(os.getenv("CHROMA_DB_DIR", DATA_DIR / "03-vector-store")).resolve()
CHROMA_COLLECTION = os.getenv("CHROMA_COLLECTION", "documentation")
EMBEDDING_MODEL_NAME = os.getenv("EMBEDDING_MODEL_NAME", "all-MiniLM-L6-v2")
MESSAGE_BROKER_URL = os.getenv("MESSAGE_BROKER_URL")  # opcional
APP_VERSION = "0.1.0"

