import pandas as pd

# Input and output paths
input_path = "/mnt/c/Apps/CIBERSORTx/rnaseq_expression_luad/rnaseq_expression_luad_copy.tsv"
output_path = "/mnt/c/Apps/CIBERSORTx/rnaseq_expression_luad/rnaseq_expression_luad_deduplicated.tsv"

# Read all lines as raw text
with open(input_path, "r", encoding="utf-8") as f:
    lines = f.readlines()

# Keep only the first occurrence of each prefix (first 2048 characters)
seen = set()
unique_lines = []
for line in lines:
    prefix = line[:2048]   # first 2048 characters
    if prefix not in seen:
        seen.add(prefix)
        unique_lines.append(line)

# Write the result to the output file
with open(output_path, "w", encoding="utf-8") as f:
    f.writelines(unique_lines)