import pandas as pd

dev_df = pd.read_parquet("./data/processed/dev.parquet")

print(dev_df.head())
print(f"Dataframe shape: {dev_df.shape}")
