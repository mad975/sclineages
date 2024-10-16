# SCLineages - Contents and Reproduction Instructions

## Overview
The repository contains the data presented in the paper: the proposal and the two case studies. We have included their contents and scripts to reproduce the data and analyses.

### Datasets Description
We have three datasets:
- **SCLineagesSet**: containing all contract lineages.
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
    - `All-contracts-lineages.csv`: This dataset contains all contract lineages. Contracts with the same `proxy` value belong to the same lineage (versions of the same contract).
    - `Open-source-contract-lineages.csv`: This dataset contains only the open-source lineages contracts.
  - **`files-level/`**: Datasets containing file-level information.
    - `solidity_files_in_open_source_contract.csv`: .
  - **`functions-level/`**: Datasets for function-level analysis.
  - **`sample-contracts-dumps/`**: Contains a sample of smart contracts extracted from the dataset, allowing for a smaller-scale examination of contract structures and behavior.

- **`Case-study-1-LSH-model-evaluation/`**: Contains scripts for evaluating the LSH model in Case Study 1.

- **`Case-study-2-Big-vul-SC/`**: Contains resources related to Case Study 2.

- **`src-reproduce-papers-contents/`**: This directory contains scripts necessary to reproduce the elements presented in the paper.

- **`src-Leverage-Sc-Lineage/`**: This directory contains scripts to leverage SCLineages to analyze and evaluate contract lineages. It includes:
  - A script to find the lineage of a contract or a list of contracts using SCLineages.
  - A script to evaluate a dataset of contract lineages. This tool allows you to input a dataset having columns `"contract"` and `"member-of-it-lineage"`.

## Dataset Requirements

Ensure that the dataset you want to evaluate has the following two columns:

- **`contract`**: This column should contain the unique contract identifier (usually an address) for each smart contract you wish to evaluate.
- **`member-of-it-lineage`**: This column should contain the identified lineage members for the contract in the same row, as determined by the model or method you are evaluating. These values should represent the lineage that the corresponding contract is considered to be part of.

Each contract listed in the `contract` column should have its corresponding lineage in the `member-of-it-lineage` column. The script will compare these lineages to those found in the SCLineages dataset to compute precision and recall metrics.

## Usage of evaluate_lineage_with_SCLineage.py

To evaluate the lineage of smart contracts, use the following command structure:

### Command Structure

```bash
python evaluate_lineage_with_SCLineage.py [dataset_to_evaluate] [-o | --open-source]

```
## Targeting Lineages
By default, the script will evaluate all contract lineages using the `All-contracts-lineages.csv` dataset. If you want to specifically target only open-source lineages, you can add the `-o` or `--open-source` flag, which uses the `Open-source-contract-lineages.csv` dataset for evaluation.

## Example: Evaluation of `test.csv` Dataset
To evaluate a dataset (`test.csv`) with the default `CONTRACT_LINEAGES_PATH`, run the following:

```bash
python evaluate_lineage_with_SCLineage.py test.csv
```
 To evaluate using the OPEN_SOURCE_CONTRACTS_PATH, add the -o flag:
```bas
python evaluate_lineage_with_SCLineage.py path/to/your/dataset/test.csv -o
```
Output
The script generates evaluation results, including overall precision and recall, based on the specified dataset. The results will be displayed  and also saved in a file.

## Evaluation Details in Case Study 2

For a comprehensive analysis of lineage evaluations and their corresponding results, please refer to **Case Study 2**. This section provides a detailed description of the methodologies employed.
