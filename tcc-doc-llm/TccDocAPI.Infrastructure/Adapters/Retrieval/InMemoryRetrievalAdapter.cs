using TccDocAPI.Domain.Ports;

namespace TccDocAPI.Infrastructure.Adapters.Retrieval;
public sealed class InMemoryRetrievalAdapter : IRetrievalPort
{
    // Troque depois por pgvector/FAISS. Aqui retornamos vazio para simplificar.
    public Task<IReadOnlyList<RetrievedChunk>> RetrieveAsync(string query, int k, CancellationToken ct = default)
        => Task.FromResult<IReadOnlyList<RetrievedChunk>>(Array.Empty<RetrievedChunk>());
}
