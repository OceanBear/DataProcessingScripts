import pandas as pd

# Parameters
N = 12  # number of rows to skip from the top of the rna_file

# Paths
gtf_file = "/mnt/c/Apps/CIBERSORTx/Homo_sapiens/Homo_sapiens.GRCh38.115.gtf"
rna_file = "/mnt/c/Apps/CIBERSORTx/rnaseq_expression_luad/rnaseq_expression_luad_raw_counts_Evie.csv"
output_file = "/mnt/c/Apps/CIBERSORTx/Homo_sapiens/filtered_gene_lengths_Evie.csv"

# Load gene list from first column of RNA file, skip first N rows
rna = pd.read_csv(rna_file, index_col=0)
genes = set(rna.index[N:])  # skip first N rows

# Storage
results = []

# Parse GTF line by line (streaming, not loading entire 3 GB file)
with open(gtf_file, "r") as f:
    for line in f:
        if line.startswith("#"):
            continue
        fields = line.strip().split("\t")
        if len(fields) < 9:
            continue
        feature_type = fields[2]
        if feature_type != "gene":
            continue

        start = int(fields[3])
        end = int(fields[4])
        attributes = fields[8]

        # Extract gene_name from attributes
        gene_name = None
        for attr in attributes.split(";"):
            attr = attr.strip()
            if attr.startswith("gene_name"):
                gene_name = attr.split('"')[1]
                break

        if gene_name and gene_name in genes:
            length = end - start + 1
            results.append((gene_name, length))

# Save to CSV
df = pd.DataFrame(results, columns=["Gene", "Length"])
df.to_csv(output_file, index=False)

print(f"Saved {df.shape[0]} genes to {output_file}")
