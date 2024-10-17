import os
import pandas as pd
import csv

# Load file mappings from the mapping file
def load_file_paths(mapping_file):
    file_paths = {}
    with open(mapping_file, 'r') as f:
        for line in f:
            key, path = line.strip().split('=')
            absolute_path = os.path.join(os.path.dirname(__file__), '..', path)
            file_paths[key] = absolute_path
    return file_paths

# Load the file mappings
file_mapping = load_file_paths('file_mapping.txt')

def get_lineages_identified(csv_file):
    """Returns the number of unique proxies in the given CSV file."""
    try:
        df = pd.read_csv(csv_file)
        return df['proxy'].nunique()
    except FileNotFoundError:
        return 0

def get_distinct_contracts(csv_file):
    """Returns the number of unique contracts in the given CSV file."""
    try:
        df = pd.read_csv(csv_file)
        return df['contract_address'].nunique()
    except FileNotFoundError:
        return 0
    except KeyError:
        return 0

def get_distinct_creators(csv_file):
    """Returns the number of unique owners in the given CSV file."""
    try:
        df = pd.read_csv(csv_file)
        return df['owner'].nunique()
    except FileNotFoundError:
        return 0

def get_pairs_predecessor_successor_contracts(csv_file):
    """Calculates the number of predecessor-successor contract pairs from the specified CSV file."""
    try:
        df = pd.read_csv(csv_file)
        df = df.sort_values(by=['proxy', 'created_on'])
        pairs = sum(len(group) - 1 for _, group in df.groupby('proxy') if len(group) > 1)
        return pairs
    except FileNotFoundError:
        return 0

def get_solidity_files_open_source_smart_contracts(csv_file):
    """Counts the number of Solidity files in the given CSV file."""
    try:
        df = pd.read_csv(csv_file)
        return df['Solidity File Path'].nunique()
    except FileNotFoundError:
        return 0
