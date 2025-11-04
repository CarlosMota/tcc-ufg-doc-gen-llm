using TccDocAPI.Domain.Ports;
using TccDocAPI.Domain.ValueObjects;

namespace TccDocAPI.Domain.Services;

public sealed class DocumentationService
{
    public string BuildPrompt(PromptTemplate template, string code, IEnumerable<RetrievedChunk> chunks)
    {
        var context = string.Join("\n\n", chunks.Select(c => c.Text));
        return template.Render(code, context);
    }
}
