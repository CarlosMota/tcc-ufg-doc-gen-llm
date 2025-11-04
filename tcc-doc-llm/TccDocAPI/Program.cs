using Microsoft.OpenApi.Models;
using TccDocAPI.Application.DependencyInjection;
using TccDocAPI.Infrastructure.DependencyInjection;
using TccDocAPI.Infrastructure.Options;
using TccDocAPI.Infrastructure.Policies;

var builder = WebApplication.CreateBuilder(args);

// Infra (adapters, http clients, policies) + Application (facades & use cases)
builder.Services.AddInfrastructure(builder.Configuration)
                .AddApplicationLayer();

builder.Services.Configure<LLMOptions>(builder.Configuration.GetSection("LLM"));
builder.Services.Configure<GroqOptions>(builder.Configuration.GetSection("Groq"));

builder.Services.AddControllers();
// Learn more about configuring Swagger/OpenAPI at https://aka.ms/aspnetcore/swashbuckle
builder.Services.AddEndpointsApiExplorer();

builder.Services.AddSwaggerGen(c =>
    c.SwaggerDoc("v1", new OpenApiInfo { Title = "DocGen-LLM API", Version = "v1" })
);
builder.Services.AddCors(p => p.AddPolicy("AllowAll",
    b => b.AllowAnyOrigin().AllowAnyHeader().AllowAnyMethod()));

var app = builder.Build();

// Configure the HTTP request pipeline.
if (app.Environment.IsDevelopment())
{
    app.UseSwagger();
    app.UseSwaggerUI();
}

app.UseCors("AllowAll");

app.UseHttpsRedirection();

app.UseAuthorization();

app.MapControllers();

if (app.Environment.IsDevelopment())
{
    app.MapGet("/", () => Results.Redirect("/swagger"));
}


app.Run();
