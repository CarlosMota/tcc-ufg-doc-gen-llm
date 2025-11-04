using System;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.DependencyInjection;
using TccDocAPI.Application.Abstractions;
using TccDocAPI.Domain.Ports;
using TccDocAPI.Infrastructure.Adapters;
using TccDocAPI.Infrastructure.Adapters.Retrieval;

// using TccDoc.Infrastructure.Adapters.Retrieval; // quando trocar pelo pgvector
using TccDocAPI.Infrastructure.Options;
using TccDocAPI.Infrastructure.Policies;

namespace TccDocAPI.Infrastructure.DependencyInjection;

public static class ServiceCollectionExtensions
{
    /// <summary>
    /// Registra infraestrutura (adapters, http clients, policies).
    /// </summary>
    public static IServiceCollection AddInfrastructure(this IServiceCollection services, IConfiguration configuration)
    {
        // Lê config
        var baseUrl = configuration["LLM:BaseUrl"] ?? "http://127.0.0.1:11434";
        services.Configure<LLMOptions>(configuration.GetSection("LLM"));

        // HttpClient para o servidor LLM (Ollama por padrão)
        services.AddHttpClient("ollama", c =>
        {
            c.BaseAddress = new Uri(baseUrl);
            c.Timeout = TimeSpan.FromMinutes(10);
        });

        // Policies/roteamento de modelos
        services.AddSingleton<IModelRoutingPolicy, DefaultRoutingPolicy>();

        // Adapters (ports)
        services.AddSingleton<ITextCompletionPort, OllamaCompletionAdapter>();
        // Troque esta linha quando tiver o adapter de retrieval “de verdade”
        services.AddSingleton<IRetrievalPort, InMemoryRetrievalAdapter>();
        // Ex.: services.AddSingleton<IRetrievalPort, PgVectorRetrievalAdapter>();

        return services;
    }
}
