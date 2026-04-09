#!/usr/bin/env python3
import pandas as pd

# Input files
selected_file = "/mnt/c/Apps/CIBERSORTx/signature_matrix/Evie_sig.csv"
available_file = "/mnt/c/Apps/CIBERSORTx/rnaseq_expression_luad/rnaseq_expression_luad_TPM_Evie.csv"

# Output file
output_file = "/mnt/c/Apps/CIBERSORTx/rnaseq_expression_luad/missing_genes_Evie.csv"

# Read first column only (keep as string)
selected_df = pd.read_csv(selected_file, usecols=[0], dtype=str)
available_df = pd.read_csv(available_file, usecols=[0], dtype=str)

# Normalize: strip spaces and drop empty values
selected_genes = (
    selected_df.iloc[:, 0]
    .dropna()
    .astype(str)
    .str.strip()
)
available_genes = (
    available_df.iloc[:, 0]
    .dropna()
    .astype(str)
    .str.strip()
)

# Use unique sets
selected_set = set(selected_genes[selected_genes != ""])
available_set = set(available_genes[available_genes != ""])

# Genes in selected but not available
missing_genes = sorted(selected_set - available_set)

# Save to CSV
out_df = pd.DataFrame({"missing_gene": missing_genes})
out_df.to_csv(output_file, index=False)

print(f"Selected genes: {len(selected_set)}")
print(f"Available genes: {len(available_set)}")
print(f"Missing genes: {len(missing_genes)}")
print(f"Output written to: {output_file}")