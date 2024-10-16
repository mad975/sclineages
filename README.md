# sclineages# SCLineages - Contents and Reproduction Instructions

## Overview
The repository contains the data presented in the paper: the proposal and the two case studies. We have included their contents and scripts to reproduce the data and analyses.

### Datasets Description
We have three datasets:
- **SCLineagesSet**:  containing all contract lineages.
- **Case Study 1 Dataset**
- **Case Study 2 Dataset**

The relationships between these datasets are as follows:
- **SCLineagesSet** is used to evaluate the dataset for **Case Study 1**.
- The dataset for **Case Study 2** is derived from **SCLineagesSet**.
- **Case Study 1** is represented in the repository by **Case-study-1-LSH-model-evaluation**.
- **Case Study 2** is represented in the repository by **Case-study-2-Big-vul-SC**.

## Repository Structure

- **`SCLineagesSet/`**: This directory contains datasets related to contract lineages, structured across three levels:
  - **`contract-Level/`**: Datasets containing information at the smart contract level.
    - `All-contracts-lineages.csv`: This dataset contains all contracts lineages.  Contracts with the same `proxy` value belong to the same lineage (versions of the same contract).
    - `Open-source-contract-lineages.csv`: This dataset contains only the open-source lineages contracts
  - **`files-level/`**: Datasets containing file-level information.
    - `solidity_files_in_open_source_contract.csv`: .
  - **`functions-level/`**: Datasets for function-level analysis.
  - **`sample-contracts-dumps/`**: Contains a sample of smart contracts extracted from the dataset, allowing for a smaller-scale examination of contract structures and behavior.

- **`Case-study-1-LSH-model-evaluation/`**: .

- **`Case-study-2-Big-vul-SC/`**: .

- **`src-reproduce-papers-contents/`**: This directory contains scripts necessary to reproduce the elements presented in the paper.

- **`src-Leverage-Sc-Lineage/`**: This directory contains scripts to leverage SCLineages to analyze and evaluate contract lineages. It includes:
  - A script to find the lineage of a contract or a list of contracts using SCLineages.
  - A script to evaluate a dataset of contract lineages. This tool allows you to input a dataset having columns `"contract" "member-of-it-lineage"` 


## Usage of evaluate_lineage_with_SCLineage.py
To evaluate the lineage of smart contracts, use the following command structure:

### Command Structure

```bash
python evaluate_lineage_with_SCLineage.py [dataset_to_evaluate] [-o | --open-source]
Example
To evaluate the dataset with the default CONTRACT_LINEAGES_PATH, use:

bash
Copy code
python evaluate_lineage_with_SCLineage.py .test.csv
If you want to evaluate using the OPEN_SOURCE_CONTRACTS_PATH instead, add the -o flag:

bash
Copy code
python evaluate_lineage_with_SCLineage.py path/to/tour/dataset/csv -o
Arguments
dataset_to_evaluate: Path to the CSV file of the dataset you wish to evaluate.
-o / --open-source: Optional flag to specify using the open-source contracts dataset for evaluation.
Output
The script generates....



