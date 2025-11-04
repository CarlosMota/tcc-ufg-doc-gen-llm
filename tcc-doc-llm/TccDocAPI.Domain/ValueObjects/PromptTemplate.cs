namespace TccDocAPI.Domain.ValueObjects;

public sealed class PromptTemplate
{
    public string Text { get; }
    
    public PromptTemplate(string text) => Text = text ?? "";

    public string Render(string code, string context) =>
        Text.Replace("{{CODE}}", code ?? "").Replace("{{CONTEXT}}", context ?? "");
}
