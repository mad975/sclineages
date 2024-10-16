import pandas as pd
import logging
import sys
from utils import (create_lineages_f2, create_lineages_ground_truth, 
                   compare_lineages_and_save_results)


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Default paths
CONTRACT_LINEAGES_PATH = '../SCLineagesSet/contract-Level/All-contracts-lineages.csv'
OPEN_SOURCE_CONTRACTS_PATH = '../SCLineagesSet/contract-Level/Open-source-contract-lineages.csv'


if len(sys.argv) < 2:
    print("Usage: python evaluate_lineage_with_SCLineage.py <dataset_to_evaluate> [-o]")
    sys.exit(1)

dataset_to_evaluate = sys.argv[1]
use_open_source = '-o' in sys.argv


if use_open_source:
    dataset_path = OPEN_SOURCE_CONTRACTS_PATH
else:
    dataset_path = CONTRACT_LINEAGES_PATH


try:
    filtered_f2 = pd.read_csv(dataset_to_evaluate)
    p5 = pd.read_csv(dataset_path)
except FileNotFoundError as e:
    logging.error(f"File not found: {e}")
    sys.exit(1)

print("Filtered F2 Columns:", filtered_f2.columns.tolist())
print("P5 Columns:", p5.columns.tolist())

# Compare lineages and save performance metrics
dummy_output_file = 'dummy_results.csv'  #
overall_precision, overall_recall, _ = compare_lineages_and_save_results(p5, filtered_f2, dummy_output_file)


performance_metrics = {
    'Overall Precision': [overall_precision],
    'Overall Recall': [overall_recall]
}

performance_df = pd.DataFrame(performance_metrics)
performance_df.to_csv('performance_metrics.csv', index=False)


print(f"Overall Precision: {overall_precision:.2f}%")
print(f"Overall Recall: {overall_recall:.2f}%")

print("Lineage comparison completed. Performance metrics saved to 'performance_metrics.csv'.")
