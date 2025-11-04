# README.md

## Requisitos Básicos

- **WSL 2 (Ubuntu recomendado)**
- **Visual Studio Code** instalado no Windows


## 1. Extensões VSCode para o projeto

Instale estas extensões no VSCode antes de começar:

- Remote - WSL
- Python (MS)
- C\# Dev Kit ou .NET SDK Support
- Node.js Extension Pack
- Docker (se necessário para containers)
- GitLens (para histórico de código)


## 2. Configuração do WSL

Abra o VSCode e conecte-se ao seu WSL (Ubuntu):

1. Abra o VSCode, pressione `F1` e execute: `Remote-WSL: New Window`
2. Atualize pacotes de sistema:

```bash
sudo apt-get update
sudo apt-get install -y ca-certificates
sudo update-ca-certificates
```


## 3. Instalação do micromamba

```bash
curl micro.mamba.pm/install.sh | bash
# Reinicie o terminal para habilitar 'micromamba'
```

Criação do ambiente:

```bash
micromamba env create -f tcc_ufg.yml
micromamba activate tcc-ufg
```

Atualização:

```bash
micromamba self-update
micromamba update --all -y
```

Listar ambientes:

```bash
micromamba env list
```


## 4. Bibliotecas Python

No ambiente:

```bash
python -m pip install --upgrade pip
pip install groq openai python-dotenv
micromamba install -y -c pytorch -c nvidia -c conda-forge pytorch pytorch-cuda=12.1
```


## 5. Instalação .NET

```bash
sudo apt-get install -y dotnet-sdk-8.0
dotnet restore
```


## 6. Instalação Node.js

```bash
sudo apt-get install -y nodejs npm
npm install
```


## 7. Ollama e LLMs Locais

Instale Ollama:

```bash
curl -fsSL https://ollama.com/install.sh | sh
sudo systemctl enable --now ollama
systemctl status ollama
```

Baixe e rode modelos:

```bash
ollama pull qwen2.5:1.5b-instruct
ollama run qwen2.5:1.5b-instruct
ollama pull deepseek-coder:6.7b-instruct-q4_K_M
ollama run deepseek-coder:6.7b-instruct-q4_K_M
```


## 8. Verifique placa de vídeo NVIDIA

```bash
nvidia-smi
```


## 9. Variáveis de ambiente

Crie `.env`:

```
GROQ_API_KEY=sua_chave_api_groq
OPENAI_API_KEY=sua_chave_api_openai
```

***

Essa configuração garante que o VSCode no WSL está pronto para desenvolvimento, com ambientes Python (micromamba), Node.js, .NET e LLMs locais funcionando juntos.

***

## 10. Arquitetura — tcc-doc-llm (Backend)

Visão geral rápida da solução tcc-doc-llm (pasta tcc-doc-llm):

- Solução: `TccDocAPI.sln`
- Projetos principais:
  - TccDocAPI (API)
    - ASP.NET Core Web API (entrypoint)
    - Program.cs, Controllers/ (ex.: LlmController .cs, WeatherForecastController.cs)
    - appsettings.json / appsettings.Development.json
    - TccDocAPI.csproj
  - TccDocAPI.Application (camada de aplicação)
    - UseCases/ (ex.: GenerateDocumentationUseCase.cs)
    - Prompts/ (Templates.cs)
    - Facade/ e DependencyInjection/ (ServiceCollectionExtensions)
    - Responsável por orquestrar fluxos e transformar entradas em chamadas de domínio/infrastructure
  - TccDocAPI.Domain (domínio)
    - Entities/, ValueObjects/, Ports/ (interfaces: IChatPort, IEmbeddingPort, IRetrievalPort, ITextCompletionPort)
    - Regras de negócio e contratos públicos entre camadas
  - TccDocAPI.Infrastructure (infraestrutura)
    - Adapters/ (ex.: OllamaChatAdapter.cs, OllamaCompletionAdapter.cs)
    - Retrieval/ (InMemoryRetrievalAdapter.cs)
    - Options/ (GroqOptions.cs, LLMOptions.cs)
    - Implementações concretas dos Ports do domínio e integração com serviços externos

Fluxo típico de chamada:
Controller (TccDocAPI) → Application/UseCase (or Facade) → Domain Ports (interfaces) → Infrastructure Adapters → Serviços externos (Ollama, Groq, embeddings, armazenamento local).

Configuração e DI:

- As classes em Options/ espelham configurações em appsettings*.json.
- A injeção de dependência é configurada em DependencyInjection/ e em ServiceCollectionExtensions para ligar Ports às implementações de Infrastructure.

Observações práticas:

- Build artifacts e pastas bin/ obj/ são gerados (existem versões em cada projeto) — não versionar.
- Variáveis de ambiente / secrets usados pela API: ex.: GROQ_API_KEY, OPENAI_API_KEY (conforme seção Variáveis de ambiente).
- Para usar modelos locais via Ollama, execute o serviço Ollama conforme README principal.

Como executar localmente (rápido):
```bash
# a partir da raiz do repositório
cd tcc-doc-llm
dotnet restore
dotnet build

# rodar a API
cd TccDocAPI
dotnet run
```

Estrutura resumida (exemplos de arquivos relevantes):
- TccDocAPI/
  - Program.cs
  - Controllers/
    - LlmController .cs
    - WeatherForecastController.cs
  - appsettings.json
- TccDocAPI.Application/
  - UseCases/GenerateDocumentationUseCase.cs
  - Prompts/Templates.cs
  - Facade/LLMFacade.cs
- TccDocAPI.Domain/
  - Entities/, ValueObjects/, Ports/
- TccDocAPI.Infrastructure/
  - Adapters/OllamaChatAdapter.cs
  - Adapters/OllamaCompletionAdapter.cs
  - Retrieval/InMemoryRetrievalAdapter.cs
  - Options/GroqOptions.cs
