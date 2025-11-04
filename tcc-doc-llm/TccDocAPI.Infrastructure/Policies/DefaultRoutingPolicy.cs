using TccDocAPI.Application.Abstractions;
using TccDocAPI.Domain.ValueObjects;

namespace TccDocAPI.Infrastructure.Policies;

public sealed class DefaultRoutingPolicy : IModelRoutingPolicy
{
    public ModelId PickForTask(LLMTask task)
    {
        // regra simples: tarefas normais usam modelo local de 7-8B
        return new ModelId("ollama", "deepseek-coder:6.7b-instruct-q4_K_M");
    }
}
