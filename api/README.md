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

## Erros comuns e correcoes

### ImportError: CXXABI_1.3.15 not found (libicui18n.so.78 / libstdc++.so.6)

Causa: o processo esta carregando o `libstdc++` do sistema em vez do `lib` do ambiente micromamba.

Solucao (recomendada):
```bash
micromamba run -n tcc-api bash -lc 'export LD_LIBRARY_PATH="$CONDA_PREFIX/lib:$LD_LIBRARY_PATH"; uvicorn app.interfaces.api:app'
```

Alternativas:
- Garanta que `libstdcxx-ng`, `libgcc-ng` e `icu` estejam atualizados no env.
- Se usa scripts/VSCode/Makefile, inclua `LD_LIBRARY_PATH="$CONDA_PREFIX/lib:$LD_LIBRARY_PATH"` no ambiente do runner.
- Tornar permanente via script de ativacao do env:
  ```bash
  micromamba activate tcc-api
  mkdir -p "$CONDA_PREFIX/etc/conda/activate.d"
  cat > "$CONDA_PREFIX/etc/conda/activate.d/ld_library_path.sh" <<'EOF'
  export LD_LIBRARY_PATH="$CONDA_PREFIX/lib:${LD_LIBRARY_PATH:-}"
  EOF
  ```

### AttributeError: np.float_ was removed in the NumPy 2.0 release

Causa: alguma dependencia nao e compativel com NumPy 2.0.

Solucao (recomendada):
```bash
micromamba install -n tcc-api -c conda-forge "numpy=1.26.*"
```

Endpoints principais (v1):
- `POST /v1/search`: consulta no repositório vetorial.
- `POST /v1/rag`: consulta + geração de resposta usando LLM.

## Testes

```bash
pytest
```

## Estrutura

- `app/config.py`: configuração (paths, coleção Chroma, modelo de embedding).
- `app/domain`: entidades e contratos (repositório vetorial, mensagens de domínio).
- `app/application/services.py`: orquestra casos de uso de consulta.
- `app/infrastructure/vector_store/`: implementação para Chroma (data/03-vector-store).
- `app/infrastructure/messaging/`: barramento simples (logging) e contrato para mensageria.
- `app/infrastructure/llm/`: cliente genérico de LLM via API compatível OpenAI.
- `app/interfaces/api.py`: endpoints FastAPI.
- `tests/`: testes unitários da aplicação.

## Variáveis úteis

- `CHROMA_DB_DIR`: caminho do persist de vetor (padrão: `../data/03-vector-store`).
- `CHROMA_COLLECTION`: nome da coleção (padrão: `documentation`).
- `EMBEDDING_MODEL_NAME`: modelo `sentence-transformers` (padrão: `all-MiniLM-L6-v2`).
- `MESSAGE_BROKER_URL`: URL para RabbitMQ (opcional, ex.: `amqp://guest:guest@localhost/`).
- `LLM_TIMEOUT_SECONDS`: timeout das chamadas LLM (padrão: `30`).
- `LLM_PROVIDERS`: lista de provedores separados por vírgula (ex.: `local,groq`).
- `LLM_DEFAULT_PROVIDER`: provedor padrão (se ausente, usa o primeiro da lista).
- `LLM_<PROVIDER>_BASE_URL`: base URL do provedor.
- `LLM_<PROVIDER>_API_KEY`: API key do provedor (se necessário).
- `LLM_<PROVIDER>_MODEL`: modelo do provedor.
