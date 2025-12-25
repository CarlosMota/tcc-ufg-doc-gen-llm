# Frontend Parser (Angular)

Gera metadados em JSON a partir de componentes Angular (.ts), produzindo um formato similar ao RoslynIndexer e já salvo na etapa `data/02-normalization/frontend-parser`.

## Pré-requisitos

- Python 3.10+ disponível no ambiente (`python3 --version`).
- Ambiente Conda/Mamba opcional usando `environment.yml` deste diretório.

### Criar ambiente com mamba

```bash
cd Indexer/frontend-parser
mamba env create -f environment.yml
mamba activate frontend-parser
```

Pacotes principais:
- `tree-sitter` / `tree-sitter-languages`: parser de TypeScript usado para ler classes Angular.

## Uso rápido

# A partir da raiz do repositório
python3 Indexer/frontend-parser/frontend_parser.py path/para/componente.component.ts
```

- Saída esperada: um arquivo JSON por método em `data/01-parser/frontend-parser`.
- Campos principais: `id`, `parser`, `source_name`, `source_path`, `namespace` (path do arquivo), `class_name`, `method_name`, `signature`, `full_context`, `content`, comentários JSDoc (`class_docs`, `method_docs`), `imports` e `metadata` do decorator `@Component` (selector, templateUrl, styleUrls, etc.).

### Exemplo de teste

Um componente de exemplo está em `Indexer/frontend-parser/examples/dashboard.component.ts`. Para gerar os metadados:

```bash
python3 Indexer/frontend-parser/frontend_parser.py Indexer/frontend-parser/examples/dashboard.component.ts
```

Os arquivos resultantes aparecerão em `data/01-parser/frontend-parser`, um por método (`ngOnInit`, `refresh`, `loadMetrics` no exemplo). O HTML correspondente (`examples/dashboard.component.html`) acompanha o template do componente para referência.

## Parâmetros opcionais

- `--parser-name`: altera o nome salvo no campo `parser` e o subdiretório padrão (default: `frontend-parser`).
- `--output-dir`: define um destino alternativo para os JSONs (por padrão usa `data/02-normalization/<parser-name>` encontrado ao subir a árvore de diretórios).

## Observações

- O parser é baseado em expressões regulares para capturar métodos dentro da classe do componente e comentários JSDoc. Estruturas muito fora do padrão Angular podem exigir ajustes.
- Constantes/readonly não são extraídos por enquanto; os campos correspondentes são preenchidos com listas vazias para manter compatibilidade com o pipeline existente.
