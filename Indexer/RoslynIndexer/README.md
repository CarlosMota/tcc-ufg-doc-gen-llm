# RoslynIndexer

Guia rápido para o projeto em C# (.NET) de indexação/análise de código.

## Pré-requisitos
- .NET SDK 8.0 instalado (verifique com `dotnet --version`).
- Ambiente Python/micromamba não é necessário aqui; use apenas o SDK do .NET.

## Como restaurar e buildar
```bash
cd Indexer/RoslynIndexer
dotnet restore
dotnet build
```

## Executar
Se houver um console app na solução:
```bash
dotnet run --project src/RoslynIndexer.Console/RoslynIndexer.Console.csproj
```
Adapte o caminho do projeto se estiver usando outra entrypoint.

## Testes
```bash
cd Indexer/RoslynIndexer
dotnet test
```

## Estrutura (essencial)
- `RoslynIndexer.sln` — solução principal.
- `src/` — projetos de produção (por exemplo, RoslynIndexer.Console, RoslynIndexer.Core).
- `tests/` — projetos de testes.
- `old/` — artefatos antigos/legados (ignorados).

## Notas
- Evite versionar pastas `bin/` e `obj/`; já estão ignoradas.
- Se precisar de configurações adicionais (ex.: caminhos de entrada/saída, connection strings), documente-as aqui conforme os projetos forem sendo estabilizados.
