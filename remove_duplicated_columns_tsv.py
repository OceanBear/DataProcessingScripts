import pandas as pd

# Input and output paths
input_path = "/mnt/f/data/public_data/TCGA/LUAD/rnaseq/raw_counts/rnaseq_expression_luad_transposed_copy.csv"
output_path = "/mnt/c/Apps/CIBERSORTx/rnaseq_expression_luad/rnaseq_expression_luad_transposed_deduplicated.tsv"

# Deduplicate columns by column name (keep the first occurrence).
df = pd.read_csv(input_path, sep=",", low_memory=False)
df.columns = df.columns.astype(str).str.strip()

before_cols = df.shape[1]
df = df.loc[:, ~df.columns.duplicated(keep="first")]
after_cols = df.shape[1]

print(f"Dropped {before_cols - after_cols} duplicated columns; kept {after_cols}.")

output_path = output_path.replace(".tsv", ".csv")
df.to_csv(output_path, sep=",", index=False)