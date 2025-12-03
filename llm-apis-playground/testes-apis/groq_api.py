import os
from groq import Groq

client = Groq(api_key=os.environ["GROQ_API_KEY"])

resp = client.chat.completions.create(
    model="llama-3.3-70b-versatile",   # <- trocado
    messages=[{"role":"user","content":"Diga 'Explique sobre Orientação Objeto'"}],
    temperature=0.2,
    # dica: se precisar limitar tokens de saída, use max_completion_tokens:
    # max_completion_tokens=256,
)
print(resp.choices[0].message.content)
