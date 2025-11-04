using TccDocAPI.Domain.ValueObjects;

namespace TccDocAPI.Application.Abstractions;
public enum TaskType { Docstring, Readme, ADR }
public enum Priority { Low, Normal, High }
public enum Quality { Low, Medium, High }

public sealed class LLMTask
{
    public TaskType Type { get; }
    public Priority Priority { get; }
    public Quality Quality { get; }
    public int MaxContextTokens { get; }
    public LLMTask(TaskType type, Priority priority, Quality quality, int maxCtx)
        { Type = type; Priority = priority; Quality = quality; MaxContextTokens = maxCtx; }

    public string QueryFrom(string code) => $"Documentar código. Tipo={Type}. Tamanho={code?.Length ?? 0}";
}
