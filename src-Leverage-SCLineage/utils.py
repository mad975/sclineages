import pandas as pd
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')



CONTRACT_LINEAGES_PATH = '../SCLineagesSet/contract-Level/All-contracts-lineages.csv'
OPEN_SOURCE_CONTRACTS_PATH = '../SCLineagesSet/contract-Level/Open-source-contract-lineages.csv'

def get_lineages_of_contract(contract_address, use_open_source=False):
    """
    Returns all contracts associated with the same proxy as the given contract address,
    formatted as c1->c2->...->cn, sorted by creation date.
    
    Parameters:
    contract_address (str): The address of the contract to find lineages for.
    use_open_source (bool): Whether to use the open-source dataset.

    Returns:
    str: A formatted string of contracts in the lineage.
    """
    file_path = OPEN_SOURCE_CONTRACTS_PATH if use_open_source else CONTRACT_LINEAGES_PATH
    df = pd.read_csv(file_path)
    
    if 'contract_address' not in df.columns:
        raise KeyError(f"The column 'contract_address' was not found in the file. Available columns: {list(df.columns)}")
    
    contract_info = df[df['contract_address'] == contract_address]

    if contract_info.empty:
        return f"No contract found with address {contract_address}."

    proxy = contract_info['proxy'].values[0]
    lineage_df = df[df['proxy'] == proxy].sort_values(by='created_on')
    lineage = '->'.join(lineage_df['contract_address'].tolist())

    return lineage







def create_lineages_f2(filtered_f2):
    if 'contract' not in filtered_f2.columns or 'member-of-it-lineage' not in filtered_f2.columns:
        raise KeyError("Expected columns not found in filtered_f2 DataFrame.")
    
    lineages_f2 = {}
    for contract in filtered_f2['contract'].unique():
        lineage = filtered_f2[filtered_f2['contract'] == contract]['member-of-it-lineage'].unique().tolist()
        if contract in lineage:
            lineage.remove(contract)  
        lineages_f2[contract] = lineage
        logging.debug(f"F2, contract: {contract}, lineage: {lineage}")
    return lineages_f2


def create_lineages_ground_truth(p5):
    lineages_GT = {}
    for contract in p5['contract_address'].unique():  
        proxy = p5[p5['contract_address'] == contract]['proxy'].values[0]  
        contracts = p5[p5['proxy'] == proxy]['contract_address'].unique().tolist()
        lineage = [c for c in contracts if c != contract]  #
        lineages_GT[contract] = lineage
        logging.debug(f"Ground truth, contract: {contract}, lineage: {lineage}")
    return lineages_GT


def compare_lineages_for_contract(lineage_GT, lineage_f2):
    tp = sum(1 for c in lineage_f2 if c in lineage_GT)  # True Positives
    fp = sum(1 for c in lineage_f2 if c not in lineage_GT)  # False Positives
    fn = sum(1 for c in lineage_GT if c not in lineage_f2)  # False Negatives
    return tp, fp, fn


def compare_lineages_and_save_results(p5, filtered_f2, output_file):
    # Create lineages from P5 and F2
    lineages_GT = create_lineages_ground_truth(p5)
    lineages_f2 = create_lineages_f2(filtered_f2)

    
    contract_results = []
    total_tp = 0
    total_fp = 0
    total_fn = 0


    for contract, lineage_GT in lineages_GT.items():
        lineage_f2 = lineages_f2.get(contract, [])
        
        tp, fp, fn = compare_lineages_for_contract(lineage_GT, lineage_f2)
        total_tp += tp
        total_fp += fp
        total_fn += fn
    
        logging.info(f"Contract: {contract}, Lineage GT: {lineage_GT}, Lineage F2: {lineage_f2}, TP: {tp}, FP: {fp}, FN: {fn}")

        contract_results.append({
            'contract': contract,
            'TP': tp,
            'FP': fp,
            'FN': fn
        })

    overall_precision = (total_tp / (total_tp + total_fp)) * 100 if (total_tp + total_fp) > 0 else 0.0
    overall_recall = (total_tp / (total_tp + total_fn)) * 100 if (total_tp + total_fn) > 0 else 0.0


    contract_results.append({
        'contract': 'Overall',
        'TP': total_tp,
        'FP': total_fp,
        'FN': total_fn,
        'precision': overall_precision,
        'recall': overall_recall
    })


    save_results_to_csv(contract_results, output_file)

    return overall_precision, overall_recall, contract_results


def save_results_to_csv(results, filename):
    df = pd.DataFrame(results)
    df.to_csv(filename, index=False)
