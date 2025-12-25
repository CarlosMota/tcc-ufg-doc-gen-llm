from fastapi import FastAPI

from .. import config
from .v1 import router as v1_router

app = FastAPI(
    title="TCC RAG API",
    version=config.APP_VERSION,
    description="API para consultas a documentos vetoriais (Chroma).",
)

app.include_router(v1_router)
