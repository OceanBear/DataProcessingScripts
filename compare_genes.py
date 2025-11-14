import csv

# File paths
lm22_file = "/mnt/c/Apps/CIBERSORTx/signature_matrix/LM22.txt"
csv_file = "/mnt/c/Apps/CIBERSORTx/rnaseq_expression_luad/rnaseq_expression_luad_TPM.csv"

# Load LM22 file (tab-separated, first column is "Gene symbol")
print("Loading LM22.txt...")
lm22_genes = set()
with open(lm22_file, 'r', encoding='utf-8') as f:
    reader = csv.reader(f, delimiter='\t')
    next(reader)  # Skip header row
    for row in reader:
        if row:  # Check if row is not empty
            gene = row[0].strip()
            if gene:  # Check if gene name is not empty
                lm22_genes.add(gene)

# Load CSV file (comma-separated, first column contains gene names)
print("Loading CSV file...")
csv_genes = set()
with open(csv_file, 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    next(reader)  # Skip header row (row 1, column 1 is usually "Gene" or "Gene symbol")
    for row in reader:
        if row:  # Check if row is not empty
            gene = row[0].strip()
            if gene:  # Check if gene name is not empty
                # Filter out purely numeric identifiers (like "1448")
                # Gene names typically contain at least one letter
                if any(c.isalpha() for c in gene):
                    csv_genes.add(gene)

# Find genes in both files
genes_in_both = lm22_genes & csv_genes

# Find genes only in LM22
genes_only_lm22 = lm22_genes - csv_genes

# Find genes only in CSV
genes_only_csv = csv_genes - lm22_genes

# Print summary
print("\n" + "="*60)
print("GENE COMPARISON SUMMARY")
print("="*60)
print(f"\nTotal genes in LM22.txt: {len(lm22_genes)}")
print(f"Total genes in CSV file: {len(csv_genes)}")
print(f"\nGenes in BOTH files: {len(genes_in_both)}")
print(f"Genes ONLY in LM22.txt: {len(genes_only_lm22)}")
print(f"Genes ONLY in CSV file: {len(genes_only_csv)}")

# Save results to files
print("\n" + "="*60)
print("SAVING RESULTS")
print("="*60)

# Save genes in both
if genes_in_both:
    both_file = "/mnt/c/ProgramData/github_repo/DataProcessingScripts/genes_in_both.txt"
    with open(both_file, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        for gene in sorted(genes_in_both):
            writer.writerow([gene])
    print(f"✓ Saved {len(genes_in_both)} genes in BOTH files to: {both_file}")

# Save genes only in LM22
if genes_only_lm22:
    only_lm22_file = "/mnt/c/ProgramData/github_repo/DataProcessingScripts/genes_only_in_LM22.txt"
    with open(only_lm22_file, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        for gene in sorted(genes_only_lm22):
            writer.writerow([gene])
    print(f"✓ Saved {len(genes_only_lm22)} genes ONLY in LM22.txt to: {only_lm22_file}")

# Save genes only in CSV
if genes_only_csv:
    only_csv_file = "/mnt/c/ProgramData/github_repo/DataProcessingScripts/genes_only_in_CSV.txt"
    with open(only_csv_file, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["Gene"])  # Header
        for gene in sorted(genes_only_csv):
            writer.writerow([gene])
    print(f"✓ Saved {len(genes_only_csv)} genes ONLY in CSV file to: {only_csv_file}")

# Print first 20 genes from each category as examples
print("\n" + "="*60)
print("SAMPLE GENES (first 20)")
print("="*60)

if genes_in_both:
    print(f"\nGenes in BOTH (showing first 20 of {len(genes_in_both)}):")
    for i, gene in enumerate(sorted(genes_in_both)[:20], 1):
        print(f"  {i}. {gene}")

if genes_only_lm22:
    print(f"\nGenes ONLY in LM22.txt (showing first 20 of {len(genes_only_lm22)}):")
    for i, gene in enumerate(sorted(genes_only_lm22)[:20], 1):
        print(f"  {i}. {gene}")

if genes_only_csv:
    print(f"\nGenes ONLY in CSV file (showing first 20 of {len(genes_only_csv)}):")
    for i, gene in enumerate(sorted(genes_only_csv)[:20], 1):
        print(f"  {i}. {gene}")

print("\n" + "="*60)
print("COMPARISON COMPLETE")
print("="*60)

