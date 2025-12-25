using System.Collections.Generic;
using System.Text.Json;
using System.Text.Json.Serialization;

namespace RoslynIndexer.Core.Models
{
    public class CodeMetadata
    {
        [JsonPropertyName("file_path")]
        public string FilePath { get; set; } = string.Empty;

        [JsonPropertyName("namespace")]
        public string Namespace { get; set; } = string.Empty;

        [JsonPropertyName("class_name")]
        public string ClassName { get; set; } = string.Empty;

        [JsonPropertyName("method_name")]
        public string MethodName { get; set; } = string.Empty;

        [JsonPropertyName("signature")]
        public string Signature { get; set; } = string.Empty;

        [JsonPropertyName("content_length")]
        public int ContentLength { get; set; }

        [JsonPropertyName("content")]
        public string Content { get; set; } = string.Empty;
        
        [JsonPropertyName("method_docs")]
        public string MethodDocumentation { get; set; } = string.Empty;

        [JsonPropertyName("class_docs")]
        public string ClassDocumentation { get; set; } = string.Empty;

        [JsonPropertyName("constants_in_scope")]
        public List<string> ConstantsInScope { get; set; } = new();

        [JsonPropertyName("readonly_fields_in_scope")]
        public List<string> ReadonlyFieldsInScope { get; set; } = new();

        [JsonPropertyName("imports")]
        public List<string> Imports { get; set; } = new();

        // O FullContext geralmente não precisa ser serializado se for apenas computado, 
        // mas pode ser útil para debug ou busca direta.
        [JsonPropertyName("full_context")]
        public string FullContext => $"{Namespace}.{ClassName}.{MethodName}";

        /// <summary>
        /// Converte a instância atual para uma string JSON formatada.
        /// </summary>
        public string ToJson()
        {
            var options = new JsonSerializerOptions 
            { 
                WriteIndented = true, // Deixa o JSON legível (formatado)
                Encoder = System.Text.Encodings.Web.JavaScriptEncoder.UnsafeRelaxedJsonEscaping // Evita escapar caracteres como <, >, + desnecessariamente
            };
            return JsonSerializer.Serialize(this, options);
        }
    }
}
