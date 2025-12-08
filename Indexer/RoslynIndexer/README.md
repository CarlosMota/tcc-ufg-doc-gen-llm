# RoslynIndexer

Guia rápido do projeto em C# (.NET) para indexação/análise de código.

## Pré-requisitos

- .NET SDK 8.0 instalado (`dotnet --version`).
- Não requer micromamba/Python para esta parte.

## Setup rápido

```bash
cd Indexer/RoslynIndexer
dotnet restore
dotnet build
```

## Executar o console

```bash
dotnet run --project src/RoslynIndexer.Console/RoslynIndexer.Console.csproj
```
Adapte o caminho se usar outro entrypoint.

## Testes

```bash
cd Indexer/RoslynIndexer
dotnet test
```

## Estrutura

- `RoslynIndexer.sln` — solução principal.
- `src/` — produção (RoslynIndexer.Console, RoslynIndexer.Core).
- `tests/` — projetos de testes.
- `old/` — artefatos legados (ignorados).

## Saída de dados

- JSONs do parser Roslyn: `data/01-parser/roslyn_output` (o app procura/gera a pasta `data` a partir do diretório atual). Ajuste no código se quiser outra etapa ou destino (ex.: `02-normalization`).

## Notas

- Não versionar `bin/` e `obj/` (já ignorados).
