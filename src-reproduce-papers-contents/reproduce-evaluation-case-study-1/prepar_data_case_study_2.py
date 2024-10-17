import pandas as pd


data = "../../Case-study-1-LSH-model-evalution/LSH-similarity-crawled-contracts-output/LSH-similar-all-levels-all-contracts.csv"
df_data = pd.read_csv(data)
print("Original Columns:", df_data.columns.tolist())
prepared_data = df_data.copy()

if prepared_data.shape[1] >= 4:
    prepared_data.columns = ['proxy', 'contract', 'member-of-it-lineage', 'level']
else:
    print("The DataFrame does not have enough columns to rename.")

print("Updated Columns:", prepared_data.columns.tolist())

output_file_path = "all-levels-all-contracts-prepared.csv"
prepared_data.to_csv(output_file_path, index=False)

print(f"Prepared data saved to: {output_file_path}")
