using TccDocAPI.Domain.ValueObjects;

namespace TccDocAPI.Domain.Ports;

public sealed record ChatMessage(string role, string content);

public sealed record ChatOptions(ModelId Model, double Temperature, int MaxTokens, int ContextSize, string KeepAlive = "30m");

public interface IChatPort
{
    Task<string> ChatAsync(IEnumerable<ChatMessage> messages, ChatOptions options, CancellationToken ct = default);
}
