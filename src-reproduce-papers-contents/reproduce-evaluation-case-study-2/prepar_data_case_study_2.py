import pandas as pd

# Load the DataFrame from the CSV file
data = "../../Case-study-1-LSH-model-evalution/LSH-similarity-crawled-contracts-output/LSH-similar-all-levels-all-contracts.csv"
df_data = pd.read_csv(data)

# Check the original columns
print("Original Columns:", df_data.columns.tolist())

# Copy the DataFrame and rename the columns
prepared_data = df_data.copy()

# Check if the DataFrame has at least 4 columns to rename
if prepared_data.shape[1] >= 4:
    prepared_data.columns = ['proxy', 'contract', 'member-of-it-lineage', 'level']
else:
    print("The DataFrame does not have enough columns to rename.")

# Print the updated DataFrame columns to verify
print("Updated Columns:", prepared_data.columns.tolist())

# Save the modified DataFrame to a new CSV file
output_file_path = "all-levels-all-contracts-prepared.csv"
prepared_data.to_csv(output_file_path, index=False)

print(f"Prepared data saved to: {output_file_path}")
