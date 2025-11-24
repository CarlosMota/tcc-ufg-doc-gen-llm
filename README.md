# README.md

## Requisitos Básicos

- **WSL 2 (Ubuntu recomendado)**
- **Visual Studio Code** instalado no Windows

## Passo 1: Instalar o WSL (Subsistema do Windows para Linux)

1. Abra o PowerShell como Administrador:
2. Busque por “PowerShell”, clique com o direito e vá em “Executar como administrador”.

Execute o comando:

```bash
wsl --install -d Ubuntu-22.04
```

Isso instala o WSL e o Ubuntu por padrão. Quando finalizar, reinicie o PC.

3. Depois de Reiniciar verificar se foi instalado corretamente usando o seguinte comando:

```bash
wsl -l -v
```

---

## Passo 2: Integração VS Code + WSL

### 1. Instalação da extensão Remote Explorer

Para editar arquivos e rodar códigos que estão dentro do Linux usando a interface do VS Code no Windows, siga estes passos:

1. Abra o VS Code no Windows.
2. Vá para a aba de Extensões (ou pressione Ctrl+Shift+X).
3. Pesquise por "Remote Explorer".
Instale a extensão oficial da Microsoft (geralmente a primeira da lista).

### 2. Acesse a Aba Remote Explorer

1. Na barra lateral esquerda do VS Code, clique no ícone Remote Explorer (parece um monitor com um sinal de `>_` ou um computadorzinho).
2. No menu dropdown (no topo da aba que abriu), selecione WSL Targets.

### 3 Conecte ao Ubuntu

1. Você verá uma lista com as distros instaladas (ex: Ubuntu-22.04).
2. Passe o mouse sobre Ubuntu-22.04 e clique no ícone de pasta com uma seta ("Connect to WSL in New Window").
3. Uma nova janela do VS Code abrirá já conectada ao seu Linux.

Dica: O Remote Explorer também mostra uma lista de Pastas Recentes que você abriu no WSL, facilitando voltar ao projeto no dia seguinte com um único clique.

---

## Passo 3: Preparar Ambiente Python para teste de RAG

Abra o VSCode e conecte-se ao seu WSL (Ubuntu):

```bash
sudo apt update && sudo apt upgrade
```

### Criar Ambiente com Micromamba (WSL)

#### 1. Instalação do micromamba

```bash
curl micro.mamba.pm/install.sh | bash
# Reinicie o terminal para habilitar 'micromamba'
```

#### 2. Criação do ambiente

```bash
micromamba env create -f tcc_ufg.yml
micromamba activate tcc-ufg
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

### Instalação .NET

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

---

<!-- ## 9. Variáveis de ambiente

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
  - Options/GroqOptions.cs -->
