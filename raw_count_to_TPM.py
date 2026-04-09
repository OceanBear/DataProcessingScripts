import pandas as pd

# Paths
rna_file = "/mnt/c/Apps/CIBERSORTx/rnaseq_expression_luad/rnaseq_expression_luad_raw_counts_Evie.csv"
length_file = "/mnt/c/Apps/CIBERSORTx/Homo_sapiens/filtered_gene_lengths_Evie.csv"
output_file = "/mnt/c/Apps/CIBERSORTx/rnaseq_expression_luad/rnaseq_expression_luad_TPM_Evie.csv"

# Load RNA raw counts (first column = genes, first row = sample IDs)
rna = pd.read_csv(rna_file, index_col=0)
rna = rna.drop(index="Gene", errors="ignore")  # remove R1C1 label if present

# Load gene lengths
lengths = pd.read_csv(length_file)
lengths = lengths.set_index("Gene")

# Keep only genes with known lengths
common_genes = rna.index.intersection(lengths.index)
rna = rna.loc[common_genes]
lengths = lengths.loc[common_genes]

# Compute Reads Per Kilobase (RPK)
rpk = rna.div(lengths["Length"] / 1000, axis=0)

# Compute scaling factor per sample
scaling = rpk.sum(axis=0) / 1e6

# Compute TPM
tpm = rpk.div(scaling, axis=1)

# Save result
tpm.to_csv(output_file)
print(f"TPM file saved with shape {tpm.shape} → {output_file}")