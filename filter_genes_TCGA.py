import pandas as pd

# This script is used to filter the genes in the RNA-seq expression file to only include the genes in the LM22 gene list.
# This is used for the TCGA dataset.
# Keep the first N rows
N = 12

# Load Evie gene list (first column only)
evie_sig_path = "/mnt/c/Apps/CIBERSORTx/signature_matrix/Evie_sig.csv"

# Read delimiter-agnostic to support both comma- and tab-separated files.
lm22 = pd.read_csv(
    evie_sig_path,
    sep=None,
    engine="python",
    index_col=0
)

# Evie_sig.csv: first column contains gene names (except the first header cell).
evie_genes = {
    str(x).strip()
    for x in lm22.index
    if pd.notna(x) and str(x).strip() != ""
}

# Load your RNA-seq mixture file
rna = pd.read_csv(
    "/mnt/c/Apps/CIBERSORTx/GSE295032_TPM/GSE295032_TPM_2.csv",
    index_col=1
)

# Identify genes present in Evie signature but missing from the expression file.
rna_genes = {str(x).strip() for x in rna.index if pd.notna(x) and str(x).strip() != ""}
missing_genes = sorted(evie_genes - rna_genes)

# Keep only rows whose index is in Evie gene list
filtered = rna[rna.index.astype(str).str.strip().isin(evie_genes)]

# Always keep the first N rows from the original file
first_n = rna.iloc[:N]

# Combine and remove any duplicates (in case overlap with LM22)
final = pd.concat([first_n, filtered]).drop_duplicates()

# Save result
final.to_csv(
    "/mnt/c/Apps/CIBERSORTx/GSE295032_TPM/GSE295032_TPM_Evie.csv"
)

missing_out_path = "/mnt/c/Apps/CIBERSORTx/GSE295032_TPM/GSE295032_missing_genes.csv"
pd.DataFrame({"gene": missing_genes}).to_csv(missing_out_path, index=False)

print(
    f"Filtered file saved with {final.shape[0]} genes (including first {N} rows). "
    f"Wrote {len(missing_genes)} missing Evie genes to: {missing_out_path}"
)
