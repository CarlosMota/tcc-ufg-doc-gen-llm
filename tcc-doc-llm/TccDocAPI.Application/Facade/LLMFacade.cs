using TccDocAPI.Application.Abstractions;
using TccDocAPI.Application.Prompts;
using TccDocAPI.Domain.Ports;
using TccDocAPI.Domain.ValueObjects;
using TccDocAPI.Domain.Services;

namespace TccDocAPI.Application.Facade;
public interface ILLMFacade
{
    Task<string> GenerateDocumentationAsync(string code, LLMTask task, CancellationToken ct = default);
}

public sealed class LLMFacade : ILLMFacade
{
    private readonly IModelRoutingPolicy _routing;
    private readonly ITextCompletionPort _completion;
    private readonly IRetrievalPort _retrieval;
    private readonly DocumentationService _doc;

    public LLMFacade(IModelRoutingPolicy routing, ITextCompletionPort completion, IRetrievalPort retrieval)
    {
        _routing = routing; _completion = completion; _retrieval = retrieval;
        _doc = new DocumentationService();
    }

    public async Task<string> GenerateDocumentationAsync(string code, LLMTask task, CancellationToken ct = default)
    {
        var chunks = await _retrieval.RetrieveAsync(task.QueryFrom(code), k: 5, ct);
        var prompt = _doc.BuildPrompt(Templates.Readme, code, chunks);

        var model = _routing.PickForTask(task);
        var options = new CompletionOptions(model, Temperature: 0.2, MaxTokens: 800, ContextSize: task.MaxContextTokens);

        return await _completion.CompleteAsync(prompt, options, ct);
    }
}
