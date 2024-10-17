# Metric Calculation for Table 1 (SCLineages Paper)

This Python script is used to compute the metrics presented in **Table 1** of the SCLineages paper.

## Main Metrics Computed

1. **Lineages Identified**: 
   - Calculates the number of unique contract lineages for both all contracts and open-source contracts.
   
2. **Distinct Contracts**:
   - Determines the number of unique contracts for both all contracts and open-source contracts.
   
3. **Predecessor-Successor Contract Pairs**:
   - Identifies the number of contract pairs where one contract is the successor of another.
   
4. **Solidity Files**:
   - Counts the number of unique Solidity files in open-source smart contracts.
   
5. **Distinct Creators**:
   - Computes the number of distinct creators/owners across all contracts.

## File Mapping

The script relies on a `file_mapping.txt` file to locate the appropriate CSV files for each metric. This ensures that the data files are correctly loaded and processed.

## Output

The computed metrics are printed in a summary and saved to a CSV file with a timestamp.

## How to Use

1. Ensure the `file_mapping.txt` file contains the correct paths to the necessary data files.
2. Run the script using Python 3.
3. The resulting metrics will be displayed and saved in a CSV file named with the current date.

This script is essential for reproducing the results presented in Table 1 of the paper, showcasing the lineage, evolution, and characteristics of smart contracts in the dataset.
