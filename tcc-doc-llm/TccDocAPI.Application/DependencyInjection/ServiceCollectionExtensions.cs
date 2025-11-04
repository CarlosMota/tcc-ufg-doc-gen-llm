using Microsoft.Extensions.DependencyInjection;
using TccDocAPI.Application.Facade;
using TccDocAPI.Application.UseCases;

namespace TccDocAPI.Application.DependencyInjection;

public static class ServiceCollectionExtensions
{
    /// <summary>
    /// Registra serviços da camada de aplicação (facades, use cases).
    /// </summary>
    public static IServiceCollection AddApplicationLayer(this IServiceCollection services)
    {
        services.AddSingleton<ILLMFacade, LLMFacade>();
        services.AddSingleton<GenerateDocumentationUseCase>();
        
        return services;
    }
}
