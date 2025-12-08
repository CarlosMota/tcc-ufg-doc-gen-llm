using System;
using System.IO; // Necessário para manipular arquivos e pastas
using Microsoft.CodeAnalysis.CSharp;
using RoslynIndexer.Core.Analyzers;
using Spectre.Console;

class Program
{
    static void Main(string[] args)
    {
        AnsiConsole.Write(new FigletText("Roslyn Indexer").Color(Color.Green));

        var dummyCode = @"
        using System;

        namespace SistemaFinanceiro.Domain
        {
            /// <summary>
            /// Responsável pelos cálculos tributários do sistema.
            /// </summary>
            public class CalculadoraImposto
            {
                private const decimal AliquotaPadraoIcms = 0.18m;

                /// <summary>
                /// Calcula o ICMS base.
                /// </summary>
                public decimal CalcularICMS(decimal valor, string estado)
                {
                    return valor * AliquotaPadraoIcms;
                }

                public void MetodoSemDoc() 
                { 
                    // ... 
                }
            }
        }";

        AnsiConsole.MarkupLine("[bold yellow]Analisando código em memória...[/]");

        var syntaxTree = CSharpSyntaxTree.ParseText(dummyCode);
        var root = syntaxTree.GetRoot();

        var collector = new RagSyntaxCollector("DummyFile.cs");
        collector.Visit(root);

        // --- LÓGICA DE SALVAMENTO ---

        // 1. Definir onde vamos salvar
        // Procura uma pasta "data" na árvore (raiz do repo) e usa um subdiretório dedicado à etapa 01-parser do Roslyn
        var outputDirectory = Path.Combine(ResolveDataDirectory(), "01-parser", "roslyn_output");

        // 2. Garantir que a pasta existe (se não, cria)
        if (!Directory.Exists(outputDirectory))
        {
            Directory.CreateDirectory(outputDirectory);
        }

        AnsiConsole.MarkupLine($"[bold]Salvando {collector.ExtractedMetadata.Count} arquivos em:[/] [blue]{outputDirectory}[/]");

        // 3. Iterar e salvar cada item
        foreach (var item in collector.ExtractedMetadata)
        {
            // Gera o JSON usando o método que criamos no CodeMetadata
            var jsonContent = item.ToJson();

            // Cria um nome de arquivo seguro (o FullContext é ótimo para garantir unicidade)
            // Substituímos < e > caso haja Generics (ex: List<T>) pois o Windows não aceita em nomes de arquivo
            var safeFileName = item.FullContext
                .Replace("<", "_")
                .Replace(">", "_")
                .Replace(" ", "") 
                + ".json";

            var fullPath = Path.Combine(outputDirectory, safeFileName);

            // Escreve o texto no disco
            File.WriteAllText(fullPath, jsonContent);
            
            AnsiConsole.MarkupLine($"  [green]✔[/] Salvo: [grey]{safeFileName}[/]");
        }

        AnsiConsole.WriteLine();
        AnsiConsole.MarkupLine("[bold green]Processo finalizado com sucesso![/]");
    }

    static string ResolveDataDirectory()
    {
        var dir = Directory.GetCurrentDirectory();
        while (!string.IsNullOrEmpty(dir))
        {
            var candidate = Path.Combine(dir, "data");
            if (Directory.Exists(candidate))
            {
                return candidate;
            }

            dir = Directory.GetParent(dir)?.FullName;
        }

        // Fallback: cria um data/ local ao diretório de execução
        var fallback = Path.Combine(Directory.GetCurrentDirectory(), "data");
        Directory.CreateDirectory(fallback);
        return fallback;
    }
}
