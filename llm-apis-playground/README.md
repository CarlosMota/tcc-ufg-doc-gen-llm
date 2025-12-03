# LLM APIs Playground

Para preparar o WSL e o VS Code, siga primeiro as instruções do README na raiz do repositório. Abaixo estão apenas os passos específicos deste subprojeto para rodar e testar as APIs LLM.

## Preparar ambiente Python para testes das APIs LLM

Abra o VSCode e conecte-se ao seu WSL (Ubuntu):

```bash
sudo apt update && sudo apt upgrade
```

### Criar ambiente com micromamba (WSL)

#### 1. Instalação do micromamba

```bash
curl micro.mamba.pm/install.sh | bash
# Reinicie o terminal para habilitar 'micromamba'
```

#### 2. Criação do ambiente

```bash
micromamba env create -f llm-apis-playground/llm-apis-tests.yml
micromamba activate llm-apis-tests
```

#### 3. Atualização

```bash
micromamba self-update
micromamba update --all -y
```

#### 4. Listar ambientes

```bash
micromamba env list
```

### Instalação .NET (somente se for trabalhar no Indexer)

```bash
sudo apt-get install -y dotnet-sdk-8.0
dotnet restore
```

## Passo 4: Baixar modelos LLMs locais

### 1. Instale Ollama:

```bash
curl -fsSL https://ollama.com/install.sh | sh
sudo systemctl enable --now ollama
systemctl status ollama
```

### 2. Baixe e rode modelos:

```bash
ollama pull qwen2.5:1.5b-instruct
ollama run qwen2.5:1.5b-instruct
ollama pull deepseek-coder:6.7b-instruct-q4_K_M
ollama run deepseek-coder:6.7b-instruct-q4_K_M
```

### 3. Execute o comando para verificar se os modelos foram baixados corretamente:

```bash
ollama list
```

### 4. Teste os modelos

```bash
./run_models.sh "Explique RAG (Retrieval-Augmented Generation), com contexto para LLM (Large Language Model)"
```

Após isso verá que foi criada uma pasta chamada outputs com os arquivos de saída dos testes.

> Observação: este ambiente `llm-apis-tests` inclui apenas dependências mínimas para subir e testar as APIs (Flask, chromadb, psycopg2 se usar Postgres e os pacotes de LLM). Adicione `numpy`, `pandas` ou `pdftotext` no `llm-apis-tests.yml` somente se realmente usar no código. Para o Indexer (.NET), use as instruções específicas na pasta `Indexer/` e um ambiente separado.
Para o Indexer em C#/.NET, consulte `Indexer/RoslynIndexer/README.md`.
