import argparse
from utils import get_lineages_of_contract

def main():
    parser = argparse.ArgumentParser(description="Find contract lineages.")
    parser.add_argument("contract_address", type=str, help="The contract address to find lineages for.")
    parser.add_argument("-o", "--open", action="store_true", help="Use the open-source contract dataset.")
    
    args = parser.parse_args()

    contract_address = args.contract_address
    use_open_source = args.open

    lineage = get_lineages_of_contract(contract_address, use_open_source)
    
    print(f"Lineage for contract {contract_address}: {lineage}")

if __name__ == "__main__":
    main()
