using System.Text.Json;

class Program
{
    static void Main(string[] args)
    {
        var baseReposFolder = "/workspace/repos_analisados";
        Directory.CreateDirectory(baseReposFolder);

        if (args.Length == 0)
        {
            Console.Error.WriteLine("Uso: RoslynIndexer <nome-da-pasta-do-repo>");
            return;
        }

        var repoName = args[0];
        var rootFolder = Path.Combine(baseReposFolder, repoName);

        if (!Directory.Exists(rootFolder))
        {
            Console.Error.WriteLine($"Pasta não encontrada: {rootFolder}");
            return;
        }

        var metadados = RoslynExtractor.ExtractMethods(rootFolder);

        var json = JsonSerializer.Serialize(
            metadados,
            new JsonSerializerOptions { WriteIndented = true }
        );

        Console.WriteLine(json);
    }
}
