using TccDocAPI.Application.Abstractions;
using TccDocAPI.Application.Facade;

namespace TccDocAPI.Application.UseCases;
public sealed class GenerateDocumentationUseCase
{
    private readonly ILLMFacade _facade;
    public GenerateDocumentationUseCase(ILLMFacade facade) => _facade = facade;

    public Task<string> ExecuteAsync(string code, CancellationToken ct = default)
    {
        var task = new LLMTask(TaskType.Readme, Priority.Normal, Quality.Medium, maxCtx: 4096);
        return _facade.GenerateDocumentationAsync(code, task, ct);
    }
}
