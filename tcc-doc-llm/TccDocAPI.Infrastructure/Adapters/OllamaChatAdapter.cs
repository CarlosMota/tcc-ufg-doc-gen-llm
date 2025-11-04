using System.Text;
using Newtonsoft.Json;
using Newtonsoft.Json.Linq;
using TccDocAPI.Domain.Ports;

namespace TccDocAPI.Infrastructure.Adapters;
public sealed class OllamaChatAdapter : IChatPort
{
    private readonly IHttpClientFactory _httpFactory;
    public OllamaChatAdapter(IHttpClientFactory httpFactory) => _httpFactory = httpFactory;

    public async Task<string> ChatAsync(IEnumerable<ChatMessage> messages, ChatOptions options, CancellationToken ct = default)
    {
        var http = _httpFactory.CreateClient("ollama");
        var payload = new
        {
            model = options.Model.Name,
            messages = messages.Select(m => new { m.role, m.content }),
            stream = false,
            options = new { temperature = options.Temperature, num_ctx = options.ContextSize, num_predict = options.MaxTokens, keep_alive = options.KeepAlive }
        };
        var json = JsonConvert.SerializeObject(payload);
        using var resp = await http.PostAsync("/api/chat", new StringContent(json, Encoding.UTF8, "application/json"), ct);
        var text = await resp.Content.ReadAsStringAsync(ct);
        resp.EnsureSuccessStatusCode();
        var data = JObject.Parse(text);
        return (string?)(data.SelectToken("message.content") ?? data["response"]) ?? string.Empty;
    }
}
