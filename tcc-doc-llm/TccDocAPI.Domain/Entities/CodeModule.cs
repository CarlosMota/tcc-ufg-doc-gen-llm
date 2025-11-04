namespace TccDocAPI.Domain.Entities;
public sealed class CodeModule
{
    public string Path { get; }
    public string Source { get; }
    public CodeModule(string path, string source) { Path = path; Source = source; }
}
