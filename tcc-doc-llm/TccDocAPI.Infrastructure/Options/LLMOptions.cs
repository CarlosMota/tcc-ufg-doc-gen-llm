namespace TccDocAPI.Infrastructure.Options;
public sealed class LLMOptions
{
    public string BaseUrl { get; set; } = "http://127.0.0.1:11434";
    public string DefaultModel { get; set; } = "deepseek-coder:6.7b-instruct-q4_K_M";
    public string KeepAlive { get; set; } = "30m";
}