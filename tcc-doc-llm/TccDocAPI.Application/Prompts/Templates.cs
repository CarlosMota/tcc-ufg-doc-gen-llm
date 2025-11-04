using TccDocAPI.Domain.ValueObjects;

namespace TccDocAPI.Application.Prompts;
public static class Templates
{
    public static readonly PromptTemplate Readme =
        new PromptTemplate(
@"Você é um gerador de documentação técnica objetiva.
Contexto adicional:
{{CONTEXT}}

Gere README (Markdown) para o módulo a partir do código:
```code
{{CODE}}
```");
}
