# Verificar langchain
import langchain; print(f'LangChain: {langchain.__version__}')

# Verificar langchain-openai
import langchain_openai; print('LangChain OpenAI: OK')

# Verificar chromadb
import chromadb; print(f'ChromaDB: {chromadb.__version__}')

# Verificar sentence-transformers
import sentence_transformers; print(f'Sentence Transformers: OK')

from pydantic import BaseModel; print(f'pydantic: OK')

# Verificar todos de uma vez

import sys
packages = ['langchain', 'langchain_openai', 'chromadb', 'sentence_transformers','pydantic']
for package in packages:
    try:
        __import__(package)
        print(f'✅ {package}: Instalado')
    except ImportError:
        print(f'❌ {package}: Não instalado')
