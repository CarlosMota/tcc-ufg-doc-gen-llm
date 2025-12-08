# Documentation Processor

Processador de documentação para análise e inserção de dados em banco vetorial.

## 📋 Pré-requisitos

- Micromamba ou Conda instalado
- Python 3.11+

## 🚀 Instalação do Ambiente

### 1. Criar o ambiente conda/micromamba

```bash
micromamba env create -f environment.yml
```

### 2. Ativar o ambiente

```bash
micromamba activate documentation-processor
```

### 3. Instalar pacotes Python adicionais via pip

⚠️ **Importante**: Instalar os pacotes na ordem abaixo para evitar conflitos de dependências:

```bash
# 1. Instalar langchain primeiro (framework base)
pip install langchain==0.1.0

# 2. Instalar integração OpenAI
pip install langchain-openai==0.0.2

# 3. Instalar ChromaDB (banco de dados vetorial)
pip install chromadb==0.4.22

# 4. Instalar Sentence Transformers (último para evitar conflitos)
pip install sentence-transformers==2.2.2

# 5. Fix de compatibilidade do huggingface
pip install "huggingface-hub<0.20.0"
```

### 4. Verificar instalação

Execute o script de verificação:

```bash
python -c "
import sys
packages = ['langchain', 'langchain_openai', 'chromadb', 'sentence_transformers']
for package in packages:
    try:
        __import__(package)
        print(f'✅ {package}: Instalado com sucesso')
    except ImportError as e:
        print(f'❌ {package}: Erro - {e}')
"
```

## 📦 Pacotes Instalados

### Dependências Conda (ambiente base):

- **python=3.11**: Linguagem Python
- **numpy**: Computação numérica
- **pandas**: Manipulação de dados
- **pydantic**: Validação de dados
- **pyyaml**: Parser YAML
- **python-dotenv**: Gerenciamento de variáveis de ambiente
- **requests**: Requisições HTTP
- **httpx**: Cliente HTTP moderno
- **aiofiles**: Suporte a arquivos assíncronos
- **tiktoken**: Tokenização para modelos OpenAI

### Dependências Pip (instalação manual):

- **langchain**: Framework para aplicações LLM
- **langchain-openai**: Integração com OpenAI
- **chromadb**: Banco de dados vetorial
- **sentence-transformers**: Modelos de embeddings

## 🔧 Solução de Problemas

### Erro: "Could not build wheels"

```bash
pip install --upgrade pip setuptools wheel
pip install package-name --no-cache-dir
```

### Erro: Conflitos de dependências

```bash
# Desinstalar tudo e reinstalar na ordem correta
pip uninstall langchain langchain-openai chromadb sentence-transformers -y
pip install langchain==0.1.0
pip install langchain-openai==0.0.2
pip install chromadb==0.4.22
pip install sentence-transformers==2.2.2
pip install "huggingface-hub<0.20.0"
```

## 🔄 Pipeline de normalização e inserção no ChromaDB

O script `documentation_processor` executa três etapas: lê os JSONs gerados pelos parsers em `data/01-parser/*`, normaliza os dados adicionando um `id`, grava em `data/02-normalization/` e insere o texto/metadata no ChromaDB.

### Executar

```bash
cd documentation-processor
python -m documentation_processor --collection documentation
```

### Estrutura esperada

- Entrada: `data/01-parser/<nome_parser>/*.json`
- Normalização: `data/02-normalization/<nome_parser>/*__<id>.json`
- Chroma persistente: `data/03-vector-store/`

### Variáveis de ambiente úteis

- `PARSER_INPUT_DIR`: caminho alternativo para as pastas de parser.
- `NORMALIZATION_DIR`: destino dos arquivos normalizados.
- `CHROMA_DB_DIR`: pasta de persistência do ChromaDB.
- `CHROMA_COLLECTION`: nome padrão da coleção (override do parâmetro `--collection`).
- `EMBEDDING_MODEL_NAME`: modelo `sentence-transformers` usado para embeddings (padrão: `all-MiniLM-L6-v2`).

### Saída salva em JSON

Cada arquivo normalizado inclui:

- `id` estável (UUID5) combinando parser + contexto + assinatura.
- Campos originais relevantes (`namespace`, `class_name`, `method_name`, `signature`, `content`, docs etc).
- `embedding_text` já concatenado (assinatura, comentários XML, código e constantes).
- `metadata` extra preservando chaves desconhecidas do parser.

### Erro: Versões incompatíveis

Use as versões especificadas acima ou consulte a documentação oficial dos pacotes.
