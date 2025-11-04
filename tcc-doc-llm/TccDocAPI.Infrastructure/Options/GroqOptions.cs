namespace TccDocAPI.Infrastructure.Options;
public sealed class GroqOptions
{
    public string BaseUrl { get; set; } = "https://api.openai.com/v1";
    public string ApiKey { get; set; } = ""; // inject via command Environment
    public string DefaultModel { get; set; } = "deepseek-coder:6.7b-instruct-q4_K_M";
}
