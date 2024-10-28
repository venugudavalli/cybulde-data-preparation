import os

import pandas as pd

cwd = os.getcwd()

# print(f"Currentworking directory: {cwd}")

test_df = pd.read_parquet("gs://abhideep/cybulde/data/processed/rebalanced_splits/dev.parquet")  # GCP
# test_df = pd.read_parquet(cwd + "/data/processed/dev.parquet") # local
print(test_df.shape)
print(test_df.columns.values)
samples_per_dataset = test_df.groupby("dataset_name").size()
print(samples_per_dataset)
