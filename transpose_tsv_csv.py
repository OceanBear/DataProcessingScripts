import pandas as pd

df = pd.read_csv("/mnt/c/Apps/CIBERSORTx/rnaseq_expression_luad/rnaseq_expression_luad.tsv", sep="\t", header=None)
df = df.transpose()
df.to_csv("/mnt/c/Apps/CIBERSORTx/rnaseq_expression_luad/rnaseq_expression_luad_transposed.csv", index=False)