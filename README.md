# Guia de preparação do ambiente (WSL)

Estas instruções preparam o ambiente base (WSL e VS Code). Para detalhes de cada subprojeto, consulte os READMEs nas respectivas pastas.

- Subprojeto Python para testes de APIs LLM: `llm-apis-playground/README.md`
- Indexer em C#/.NET: `Indexer/RoslynIndexer/README.md`
- Processador de documentação e vetor: `documentation-processor/README.md`
- API RAG (FastAPI): `api/README.md`

## Requisitos básicos

- WSL 2 (Ubuntu recomendado)
- Visual Studio Code instalado no Windows

## Passo 1: Instalar o WSL (Subsistema do Windows para Linux)

1. Abra o PowerShell como Administrador.
2. Execute:

```bash
wsl --install -d Ubuntu-22.04
```

Reinicie o PC após a instalação.

3. Verifique:

```bash
wsl -l -v
```

## Passo 2: Integração VS Code + WSL

1. No VS Code (Windows), instale a extensão "Remote Explorer".
2. Abra a aba Remote Explorer, escolha WSL Targets.
3. Passe o mouse sobre `Ubuntu-22.04` e clique em “Connect to WSL in New Window”.

Dica: a aba Remote Explorer mostra pastas recentes do WSL para reabrir projetos rapidamente.

## Ordem recomendada para rodar os projetos

1) **Indexer (.NET)**: gerar os JSONs de parser em `data/01-parser/` (ver `Indexer/RoslynIndexer/README.md`).
2) **Documentation Processor (Python)**: normalizar e popular o Chroma em `data/03-vector-store/` (ver `documentation-processor/README.md`).
3) **API RAG (FastAPI)**: subir a API que consulta o vetor (ver `api/README.md`).

Links diretos:
- Documentation Processor: `documentation-processor/README.md`
- API RAG: `api/README.md`
