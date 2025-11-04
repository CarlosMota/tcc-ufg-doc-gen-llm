namespace TccDocAPI.Domain.Ports;

public sealed record RetrievedChunk(string Id, string Text, double Score, string SourcePath);

public interface IRetrievalPort
{
    Task<IReadOnlyList<RetrievedChunk>> RetrieveAsync(string query, int k, CancellationToken ct = default);
}
