import pandas as pd

# This script is used to filter the genes in the RNA-seq expression file to only include the genes in the LM22 gene list.
# This is used for the TCGA dataset.
# Keep the first N rows
N = 12

# Load LM22 gene list (first column only)
lm22 = pd.read_csv(
    "/mnt/c/Apps/CIBERSORTx/rnaseq_expression_luad/LM22.txt",
    sep="\t",
    index_col=0
)
lm22_genes = set(lm22.index)

# Load your RNA-seq mixture file
rna = pd.read_csv(
    "/mnt/c/Apps/CIBERSORTx/rnaseq_expression_luad/rnaseq_expression_luad_deduplicated_transposed.csv",
    index_col=0
)

# Keep only rows whose index is in LM22 gene list
filtered = rna[rna.index.isin(lm22_genes)]

# Always keep the first N rows from the original file
first_n = rna.iloc[:N]

# Combine and remove any duplicates (in case overlap with LM22)
final = pd.concat([first_n, filtered]).drop_duplicates()

# Save result
final.to_csv(
    "/mnt/c/Apps/CIBERSORTx/rnaseq_expression_luad/rnaseq_expression_luad_filtered.csv"
)
print(f"Filtered file saved with {final.shape[0]} genes (including first {N} rows).")
