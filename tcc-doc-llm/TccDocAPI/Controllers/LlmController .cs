using Microsoft.AspNetCore.Mvc;
using TccDocAPI.Application.UseCases;

namespace TccDocApi.Api.Controllers;

[ApiController]
[Route("api/llm")]
public sealed class LlmController : ControllerBase
{
    private readonly GenerateDocumentationUseCase _generateDoc;

    public LlmController(GenerateDocumentationUseCase generateDoc) => _generateDoc = generateDoc;

    public sealed record GenerateRequest(string code);

    [HttpPost("docs/generate")]
    public async Task<IActionResult> Generate([FromBody] GenerateRequest req, CancellationToken ct)
    {
        if (string.IsNullOrWhiteSpace(req.code)) return BadRequest("code vazio.");
        var md = await _generateDoc.ExecuteAsync(req.code, ct);
        return Ok(new { markdown = md });
    }

    [HttpGet("health")]
    public IActionResult Health() => Ok(new { ok = true });
}
