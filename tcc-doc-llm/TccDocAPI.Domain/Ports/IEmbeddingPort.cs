using TccDocAPI.Domain.ValueObjects;

namespace TccDocAPI.Domain.Ports;

public sealed record EmbeddingOptions(ModelId Model);

public interface IEmbeddingPort
{
    Task<float[]> EmbedAsync(string text, EmbeddingOptions options, CancellationToken ct = default);
    
    Task<float[][]> EmbedBatchAsync(IEnumerable<string> texts, EmbeddingOptions options, CancellationToken ct = default);
}
