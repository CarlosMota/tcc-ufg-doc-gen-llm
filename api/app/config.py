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
LLM_TIMEOUT_SECONDS = float(os.getenv("LLM_TIMEOUT_SECONDS", "30"))
LLM_PROVIDERS = [
    item.strip()
    for item in os.getenv("LLM_PROVIDERS", "local").split(",")
    if item.strip()
]
LLM_DEFAULT_PROVIDER = os.getenv("LLM_DEFAULT_PROVIDER")


def get_llm_provider_settings(provider: str) -> dict:
    prefix = f"LLM_{provider.upper()}_"
    base_url = os.getenv(f"{prefix}BASE_URL", "http://localhost:8001/v1")
    api_key = os.getenv(f"{prefix}API_KEY")
    model = os.getenv(f"{prefix}MODEL")
    print(
        f"[config] LLM settings for '{provider}': BASE_URL={base_url}, API_KEY={'SET' if api_key else 'None'}, MODEL={model}"
    )
    return {
        "base_url": base_url,
        "api_key": api_key,
        "model": model,
    }
APP_VERSION = "0.1.0"
