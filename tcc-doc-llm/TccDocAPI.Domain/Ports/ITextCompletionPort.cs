using TccDocAPI.Domain.ValueObjects;

namespace TccDocAPI.Domain.Ports;

public sealed record CompletionOptions(ModelId Model, double Temperature, int MaxTokens, int ContextSize, string KeepAlive = "30m");

public interface ITextCompletionPort
{
    Task<string> CompleteAsync(string prompt, CompletionOptions options, CancellationToken ct = default);
}
