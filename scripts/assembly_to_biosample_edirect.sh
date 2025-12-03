#!/usr/bin/env bash
set -euo pipefail

ASSEMBLIES="CMM_genome.txt"
OUTFILE="assembly_to_biosample_edirect_CMM.tsv"

echo -e "assembly\tbiosample\torganism_name" > "${OUTFILE}"

n=0
while IFS= read -r asm_raw; do
  asm=$(echo "$asm_raw" | tr -d '\r' | sed 's/^[[:space:]]*//;s/[[:space:]]*$//')
  if [[ -z "$asm" ]]; then
    echo "[DEBUG] skipping empty line" >&2
    continue
  fi
  n=$((n+1))
  echo "[INFO] (#$n) Processing assembly: '$asm'"

  # redirect esearch input from /dev/null so it doesn't consume the file
  result=$(esearch -db assembly -query "$asm" < /dev/null | efetch -format docsum)

  biosample=$(echo "$result" | xtract -pattern DocumentSummary -element BioSampleAccn)
  organism=$(echo "$result" | xtract -pattern DocumentSummary -element OrganismName)
  if [[ -z "$biosample" ]]; then biosample="NA"; fi
  if [[ -z "$organism" ]]; then organism="NA"; fi

  echo -e "$asm\t$biosample\t$organism" >> "${OUTFILE}"
done < "${ASSEMBLIES}"

echo "[INFO] Processed total $n assemblies."
echo "[DONE] Results in ${OUTFILE}"
