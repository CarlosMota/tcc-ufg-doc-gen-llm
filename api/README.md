# API RAG (FastAPI + DDD)

API para consulta a documentos vetoriais (Chroma) com estrutura em camadas (DDD) e suporte a mensageria.

## Ambiente (micromamba)

```bash
cd api
micromamba env create -f environment-api.yml
micromamba activate tcc-api

# Instalar dependências via pip (fora do YAML)
pip install langchain==0.1.0
pip install langchain-openai==0.0.2
pip install chromadb==0.4.22
pip install sentence-transformers==2.2.2
pip install "huggingface-hub<0.20.0"
```

## Rodar a API

```bash
uvicorn app.interfaces.api:app --reload
# Swagger em: http://127.0.0.1:8000/docs
```

## Testes

```bash
pytest
```

## Estrutura

- `app/config.py`: configuração (paths, coleção Chroma, modelo de embedding).
- `app/domain`: entidades e contratos (repositório vetorial, mensagens de domínio).
- `app/application/services.py`: orquestra casos de uso de consulta.
- `app/infrastructure/vector_repository.py`: implementação para Chroma (data/03-vector-store).
- `app/infrastructure/messaging.py`: barramento simples (logging) e contrato para mensageria.
- `app/interfaces/api.py`: endpoints FastAPI.
- `tests/`: testes unitários da aplicação.

## Variáveis úteis

- `CHROMA_DB_DIR`: caminho do persist de vetor (padrão: `../data/03-vector-store`).
- `CHROMA_COLLECTION`: nome da coleção (padrão: `documentation`).
- `EMBEDDING_MODEL_NAME`: modelo `sentence-transformers` (padrão: `all-MiniLM-L6-v2`).
- `MESSAGE_BROKER_URL`: URL para RabbitMQ (opcional, ex.: `amqp://guest:guest@localhost/`).
