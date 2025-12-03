#!/usr/bin/env bash
set -euo pipefail

PROMPT=${1:-"Oi, tudo bem?"}
FILTER=${2:-""}   # se não passar nada, fica vazio

OUTDIR="outputs"
mkdir -p "$OUTDIR"

summary="$OUTDIR/summary.csv"
if [ ! -f "$summary" ]; then
  echo "RUN_ID;timestamp;model;elapsed_seconds;prompt" > "$summary"
fi

echo "Running with prompt: $PROMPT"

if [ -z "$FILTER" ]; then
  # Sem filtro: pega todos os modelos
  mapfile -t models < <(ollama list | awk 'NR>1 {print $1}')
else
  # Com filtro: só modelos cujo nome contém o filtro
  mapfile -t models < <(ollama list | awk -v f="$FILTER" 'NR>1 && $1 ~ f {print $1}')
fi


if [ ${#models[@]} -eq 0 ]; then
  echo "Nenhum modelo encontrado pelo 'ollama list'."
  exit 1
fi

RUN_ID=$(date +%Y%m%d%H%M%S)

for model in "${models[@]}"; do
  echo "==========================================="
  echo ">>> Rodando modelo: $model"
  echo "==========================================="

  # Deixa o nome do arquivo "amigável" (troca : e / por _)
  safe_name=${model//[:\/]/_}
  outfile="$OUTDIR/${safe_name}.log"
  start=$(date +%s)

  {
    echo "==========================================="
    echo "Modelo: $model"
    echo "Prompt: $PROMPT"
    echo "Data: $(date)"
    echo "-------------------------------------------"
    ollama run "$model" "$PROMPT"
    end=$(date +%s)
    elapsed=$((end - start))
    echo "-------------------------------------------"
    echo "Tempo de resposta: ${elapsed} segundos"
    timestamp=$(date --iso-8601=seconds)
    #timestamp=$(date +%Y-%m-%d_%H:%M:%S)
    echo "${RUN_ID};${timestamp};${model};${elapsed};${PROMPT}" >> "$summary"
    echo -e "\n\n"
  } | tee -a "$outfile"
done
echo "Todos os modelos foram executados. Resultados em '$OUTDIR/'."