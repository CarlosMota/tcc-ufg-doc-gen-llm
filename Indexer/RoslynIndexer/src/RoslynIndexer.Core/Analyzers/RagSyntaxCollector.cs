using System.Collections.Generic;
using System.Linq;
using Microsoft.CodeAnalysis;
using Microsoft.CodeAnalysis.CSharp;
using Microsoft.CodeAnalysis.CSharp.Syntax;
using RoslynIndexer.Core.Models;

namespace RoslynIndexer.Core.Analyzers
{
    public class RagSyntaxCollector : CSharpSyntaxWalker
    {
        public List<CodeMetadata> ExtractedMetadata { get; } = new List<CodeMetadata>();

        private string _currentNamespace = "Global";
        private string _currentClass = "Unknown";
        private string _currentClassDocumentation = "";
        private List<string> _currentClassConstants = new List<string>();
        private List<string> _currentClassReadonlyFields = new List<string>();
        private HashSet<string> _imports = new HashSet<string>();
        private readonly string _filePath;

        public RagSyntaxCollector(string filePath)
        {
            _filePath = filePath;
        }

        public override void VisitCompilationUnit(CompilationUnitSyntax node)
        {
            foreach (var usingDirective in node.Usings)
            {
                var text = usingDirective.ToString().Trim();
                _imports.Add(text);
            }
            base.VisitCompilationUnit(node);
        }

        public override void VisitNamespaceDeclaration(NamespaceDeclarationSyntax node)
        {
            var previousNamespace = _currentNamespace;
            _currentNamespace = node.Name.ToString();

            base.VisitNamespaceDeclaration(node);

            _currentNamespace = previousNamespace;
        }

        public override void VisitFileScopedNamespaceDeclaration(FileScopedNamespaceDeclarationSyntax node)
        {
            _currentNamespace = node.Name.ToString();
            base.VisitFileScopedNamespaceDeclaration(node);
        }

        public override void VisitClassDeclaration(ClassDeclarationSyntax node)
        {
            var previousClass = _currentClass;
            var previousClassDoc = _currentClassDocumentation;
            var previousConstants = _currentClassConstants;
            var previousReadonly = _currentClassReadonlyFields;

            _currentClass = node.Identifier.Text;
            _currentClassDocumentation = GetXmlDocs(node);
            _currentClassConstants = new List<string>();
            _currentClassReadonlyFields = new List<string>();

            base.VisitClassDeclaration(node);

            _currentClass = previousClass;
            _currentClassDocumentation = previousClassDoc;
            _currentClassConstants = previousConstants;
            _currentClassReadonlyFields = previousReadonly;
        }

        public override void VisitFieldDeclaration(FieldDeclarationSyntax node)
        {
            var hasConst = node.Modifiers.Any(SyntaxKind.ConstKeyword);
            var hasReadonly = node.Modifiers.Any(SyntaxKind.ReadOnlyKeyword);

            if (hasConst || hasReadonly)
            {
                foreach (var variable in node.Declaration.Variables)
                {
                    var modifierText = string.Join(" ", node.Modifiers.Select(m => m.Text));
                    var declarationText = $"{modifierText} {node.Declaration.Type} {variable.Identifier.Text}".Trim();

                    if (variable.Initializer is not null)
                    {
                        declarationText += $" = {variable.Initializer.Value}";
                    }

                    if (hasConst)
                    {
                        _currentClassConstants.Add(declarationText);
                    }

                    if (hasReadonly)
                    {
                        _currentClassReadonlyFields.Add(declarationText);
                    }
                }
            }

            base.VisitFieldDeclaration(node);
        }

        public override void VisitMethodDeclaration(MethodDeclarationSyntax node)
        {
            // --- LIMPEZA DO CONTEÚDO ---
            // Criamos uma versão "limpa" do nó removendo especificamente os comentários de documentação XML
            // Mantemos outros trivias (como espaços e indentação) para o código continuar legível
            var cleanNode = node.WithLeadingTrivia(
                node.GetLeadingTrivia()
                    .Where(t => !t.IsKind(SyntaxKind.SingleLineDocumentationCommentTrivia) && 
                                !t.IsKind(SyntaxKind.MultiLineDocumentationCommentTrivia))
            );

            var finalContent = cleanNode.ToFullString().Trim();

            var metadata = new CodeMetadata
            {
                FilePath = _filePath,
                Namespace = _currentNamespace,
                ClassName = _currentClass,
                MethodName = node.Identifier.Text,
                
                Signature = $"{node.ReturnType} {node.Identifier.Text}{node.ParameterList}",
                ConstantsInScope = _currentClassConstants.ToList(),
                ReadonlyFieldsInScope = _currentClassReadonlyFields.ToList(),
                
                // Agora usamos o cleanNode para gerar o conteúdo sem o XML repetido
                Content = finalContent, 
                ContentLength = finalContent.Length,
                MethodDocumentation = GetXmlDocs(node),
                ClassDocumentation = _currentClassDocumentation,
                Imports = _imports.ToList()
            };

            ExtractedMetadata.Add(metadata);

            base.VisitMethodDeclaration(node);
        }

        private string GetXmlDocs(CSharpSyntaxNode node)
        {
            var trivia = node.GetLeadingTrivia()
                .Select(i => i.GetStructure())
                .OfType<DocumentationCommentTriviaSyntax>()
                .FirstOrDefault();

            if (trivia == null) return string.Empty;

            return trivia.Content.ToString()
                .Replace("///", "")
                .Replace("<summary>", "")
                .Replace("</summary>", "")
                .Trim();
        }
    }
}
