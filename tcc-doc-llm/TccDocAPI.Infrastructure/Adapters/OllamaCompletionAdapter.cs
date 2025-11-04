using System.Text;
using Newtonsoft.Json;
using Newtonsoft.Json.Linq;
using TccDocAPI.Domain.Ports;
using TccDocAPI.Domain.ValueObjects;

namespace TccDocAPI.Infrastructure.Adapters;
public sealed class OllamaCompletionAdapter : ITextCompletionPort
{
    private readonly IHttpClientFactory _httpFactory;
    
    public OllamaCompletionAdapter(IHttpClientFactory httpFactory) => _httpFactory = httpFactory;

    public async Task<string> CompleteAsync(string prompt, CompletionOptions options, CancellationToken ct = default)
    {
        var http = _httpFactory.CreateClient("ollama");
        var payload = new
        {
            model = options.Model.Name,
            prompt,
            stream = false,
            options = new {
                temperature = options.Temperature,
                num_ctx = options.ContextSize,
                num_predict = options.MaxTokens,
                keep_alive = options.KeepAlive
            }
        };
        var json = JsonConvert.SerializeObject(payload);
        using var resp = await http.PostAsync("/api/generate",
            new StringContent(json, Encoding.UTF8, "application/json"), ct);
        var text = await resp.Content.ReadAsStringAsync(ct);
        resp.EnsureSuccessStatusCode();
        var data = JObject.Parse(text);
        return (string?)data["response"] ?? string.Empty;
    }
}
