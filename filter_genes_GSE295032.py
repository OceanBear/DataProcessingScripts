import json
import csv
from collections import OrderedDict

# File paths
lm22_file = "/mnt/c/Apps/CIBERSORTx/signature_matrix/LM22.txt"
gse_file = "/mnt/c/Apps/CIBERSORTx/GSE295032_TPM/GSE295032_TPM - Copy.csv"
gene_dict_file = "/mnt/c/ProgramData/github_repo/DataProcessingScripts/gene_names_dictionary.json"
output_file = "/mnt/c/Apps/CIBERSORTx/GSE295032_TPM/GSE295032_TPM_filtered.csv"
report_file = "/mnt/c/ProgramData/github_repo/DataProcessingScripts/gene_filtering_report.txt"

print("="*60)
print("GENE FILTERING SCRIPT")
print("="*60)

# Load gene names dictionary
print("\nLoading gene names dictionary...")
with open(gene_dict_file, 'r', encoding='utf-8') as f:
    gene_dict = json.load(f)

# Load LM22 gene list
print("Loading LM22.txt...")
lm22_genes = set()
with open(lm22_file, 'r', encoding='utf-8') as f:
    reader = csv.reader(f, delimiter='\t')
    next(reader)  # Skip header row
    for row in reader:
        if row:
            gene = row[0].strip()
            if gene:
                lm22_genes.add(gene)
print(f"  Found {len(lm22_genes)} genes in LM22")

# Load GSE295032 TPM file
print("Loading GSE295032_TPM file...")
gse_data = OrderedDict()  # Preserve order
gse_genes = set()
with open(gse_file, 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    header = next(reader)  # Get header row
    for row in reader:
        if row:
            gene = row[0].strip()
            if gene and any(c.isalpha() for c in gene):  # Filter out numeric-only identifiers
                gse_genes.add(gene)
                gse_data[gene] = row  # Store full row
print(f"  Found {len(gse_genes)} genes in GSE295032_TPM file")

# Track gene mappings and status
gene_mapping = {}  # Maps preferred_name to actual gene name in GSE file
genes_only_in_lm22 = []
genes_found_with_different_names = []  # List of (lm22_name, preferred_name, gse_name)

# Process each LM22 gene
print("\nProcessing LM22 genes...")
for lm22_gene in sorted(lm22_genes):
    # Get preferred name
    if lm22_gene in gene_dict:
        preferred_name = gene_dict[lm22_gene].get("preferred_name", lm22_gene)
    else:
        preferred_name = lm22_gene
    
    # Try to find the gene in GSE file
    found = False
    gse_name_used = None
    
    # First, try direct match (LM22 name in GSE file)
    if lm22_gene in gse_genes:
        gene_mapping[preferred_name] = lm22_gene
        found = True
        gse_name_used = lm22_gene
        # Only report as different if preferred_name is different from LM22 name
        # (meaning we'll use preferred_name in output but found it as LM22 name)
        if lm22_gene != preferred_name:
            genes_found_with_different_names.append((lm22_gene, preferred_name, lm22_gene))
    
    # If not found, try preferred name
    if not found and preferred_name in gse_genes:
        gene_mapping[preferred_name] = preferred_name
        found = True
        gse_name_used = preferred_name
        # Report as different if LM22 name differs from preferred name
        if lm22_gene != preferred_name:
            genes_found_with_different_names.append((lm22_gene, preferred_name, preferred_name))
    
    # If not found, try current official symbol
    if not found and lm22_gene in gene_dict:
        current_symbol = gene_dict[lm22_gene].get("current_official_symbol")
        if current_symbol and current_symbol in gse_genes:
            gene_mapping[preferred_name] = current_symbol
            found = True
            gse_name_used = current_symbol
            # Found under current symbol, which is different from LM22 name
            genes_found_with_different_names.append((lm22_gene, preferred_name, current_symbol))
    
    # If not found, try aliases
    if not found and lm22_gene in gene_dict:
        for alias in gene_dict[lm22_gene].get("aliases", []):
            if alias in gse_genes:
                gene_mapping[preferred_name] = alias
                found = True
                gse_name_used = alias
                # Found under alias, which is different from LM22 name
                genes_found_with_different_names.append((lm22_gene, preferred_name, alias))
                break
    
    # If still not found, add to genes_only_in_lm22
    if not found:
        genes_only_in_lm22.append((lm22_gene, preferred_name))

print(f"  Found {len(gene_mapping)} genes in GSE file")
print(f"  {len(genes_only_in_lm22)} genes only in LM22")
print(f"  {len(genes_found_with_different_names)} genes found with different names")

# Create filtered file with preferred names
print("\nCreating filtered file...")
if gene_mapping:
    with open(output_file, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        # Write header with preferred name as first column
        writer.writerow([header[0]] + header[1:])
        # Write data rows with preferred names
        for preferred_name, gse_name in sorted(gene_mapping.items()):
            if gse_name in gse_data:
                row = list(gse_data[gse_name])  # Create a copy of the row
                row[0] = preferred_name  # Replace gene name with preferred name
                writer.writerow(row)
    print(f"  Saved {len(gene_mapping)} genes to filtered file: {output_file}")
else:
    print("WARNING: No genes found to save!")

# Generate report
print(f"\nGenerating report to: {report_file}")
with open(report_file, 'w', encoding='utf-8') as f:
    f.write("="*60 + "\n")
    f.write("GENE FILTERING REPORT\n")
    f.write("="*60 + "\n\n")
    
    f.write(f"Total genes in LM22: {len(lm22_genes)}\n")
    f.write(f"Total genes in GSE295032_TPM: {len(gse_genes)}\n")
    f.write(f"Genes found and filtered: {len(gene_mapping)}\n")
    f.write(f"Genes only in LM22: {len(genes_only_in_lm22)}\n")
    f.write(f"Genes found with different names: {len(genes_found_with_different_names)}\n\n")
    
    # Genes only in LM22
    f.write("="*60 + "\n")
    f.write("GENES ONLY IN LM22 (NOT FOUND IN GSE295032_TPM)\n")
    f.write("="*60 + "\n")
    f.write("LM22 Name\tPreferred Name\n")
    for lm22_name, preferred_name in sorted(genes_only_in_lm22):
        f.write(f"{lm22_name}\t{preferred_name}\n")
    
    # Genes found with different names
    f.write("\n" + "="*60 + "\n")
    f.write("GENES FOUND WITH DIFFERENT NAMES\n")
    f.write("="*60 + "\n")
    f.write("LM22 Name\tPreferred Name\tGSE295032 Name\n")
    for lm22_name, preferred_name, gse_name in sorted(genes_found_with_different_names):
        f.write(f"{lm22_name}\t{preferred_name}\t{gse_name}\n")

print("\n" + "="*60)
print("FILTERING COMPLETE")
print("="*60)
print(f"\nFiltered file: {output_file}")
print(f"Report file: {report_file}")

