using TccDocAPI.Domain.ValueObjects;

namespace TccDocAPI.Application.Abstractions;

public interface IModelRoutingPolicy
{
    ModelId PickForTask(LLMTask task);
}
