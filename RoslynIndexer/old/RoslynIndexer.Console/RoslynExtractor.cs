using Microsoft.CodeAnalysis.CSharp;
using Microsoft.CodeAnalysis.CSharp.Syntax;

public static class RoslynExtractor
{
    public static List<MethodMetadata> ExtractMethods(string rootFolder)
    {
        var projeto = new DirectoryInfo(rootFolder).Name;
        var csFiles = Directory.EnumerateFiles(rootFolder, "*.cs", SearchOption.AllDirectories);

        var metadados = new List<MethodMetadata>();

        foreach (var file in csFiles)
        {
            var code = File.ReadAllText(file);

            var tree = CSharpSyntaxTree.ParseText(code);
            var root = tree.GetRoot();

            var classNodes = root.DescendantNodes().OfType<ClassDeclarationSyntax>();

            foreach (var cls in classNodes)
            {
                var className = cls.Identifier.Text;

                var nsNode = cls.Ancestors().OfType<NamespaceDeclarationSyntax>().FirstOrDefault();
                var nsName = nsNode?.Name.ToString() ?? "(global)";

                var methodNodes = cls.Members.OfType<MethodDeclarationSyntax>();

                foreach (var method in methodNodes)
                {
                    var methodName = method.Identifier.Text;

                    var firstParam = method.ParameterList.Parameters.FirstOrDefault();
                    var filterClass = firstParam?.Type?.ToString();

                    metadados.Add(new MethodMetadata
                    {
                        Arquivo = Path.GetFileName(file),
                        Classe = className,
                        Metodo = methodName,
                        Namespace = nsName,
                        Projeto = projeto,
                        FiltroClasse = filterClass
                    });
                }
            }
        }

        return metadados;
    }
}
