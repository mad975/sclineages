import pandas as pd
import datetime
import os

from getter_at_data import (
    get_lineages_identified,
    get_distinct_creators,  
    get_pairs_predecessor_successor_contracts,
    get_solidity_files_open_source_smart_contracts,
    get_distinct_contracts
)

def load_file_paths(mapping_file):
    file_paths = {}
    with open(mapping_file, 'r') as f:
        for line in f:
            key, value = line.strip().split('=')
            file_paths[key] = value
    return file_paths

def main():
    try:
        # Load file paths from the mapping file
        file_paths = load_file_paths('file_mapping.txt')
        CONTRACT_LINEAGES = file_paths['CONTRACT_LINEAGES']
        OPEN_SOURCE_CONTRACTS = file_paths['OPEN_SOURCE_CONTRACTS']
        SOLIDITY_FILES = file_paths['SOLIDITY_FILES']
        SOLIDITY_PAIR = file_paths['SOLIDITY_PAIR']

        # Collect metrics
        metrics = {
            "Lineages Identified (All Contracts)": get_lineages_identified(CONTRACT_LINEAGES),
            "Lineages Identified (Open Source Contracts)": get_lineages_identified(OPEN_SOURCE_CONTRACTS),
            "Distinct Contracts (All Contracts)": get_distinct_contracts(CONTRACT_LINEAGES),
            "Distinct Contracts (Open Source Contracts)": get_distinct_contracts(OPEN_SOURCE_CONTRACTS),
            "Predecessor-Successor (All Contracts)": get_pairs_predecessor_successor_contracts(CONTRACT_LINEAGES),
            "Total Solidity Files in Open Source Contracts": get_solidity_files_open_source_smart_contracts(SOLIDITY_FILES),
            "Distinct creator of contract": get_distinct_creators(CONTRACT_LINEAGES)
        }

        # Create DataFrame from metrics
        df = pd.DataFrame(list(metrics.items()), columns=["Metric", "Value"])

        # Print summary of metrics
        print("\nMetrics Summary:\n")
        print(df)

        # D results
        result_dir = os.path.join(os.path.dirname(__file__))


        #os.makedirs(result_dir, exist_ok=True)

        # Save results  with a timestamp
        current_date = datetime.datetime.now().strftime("%Y-%m-%d")
        result_filename = os.path.join(result_dir, f"result_{current_date}.csv")
        df.to_csv(result_filename, index=False)
        print(f"\nResults saved to {result_filename}")

    except FileNotFoundError as e:
        print(f"File not found: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
