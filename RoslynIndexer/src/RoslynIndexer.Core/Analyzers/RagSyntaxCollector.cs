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
        private readonly string _filePath;

        public RagSyntaxCollector(string filePath)
        {
            _filePath = filePath;
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

            _currentClass = node.Identifier.Text;
            _currentClassDocumentation = GetXmlDocs(node);

            base.VisitClassDeclaration(node);

            _currentClass = previousClass;
            _currentClassDocumentation = previousClassDoc;
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
                
                // Agora usamos o cleanNode para gerar o conteúdo sem o XML repetido
                Content = finalContent, 
                ContentLength = finalContent.Length,
                MethodXmlDocumentation = GetXmlDocs(node),
                ClassXmlDocumentation = _currentClassDocumentation
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