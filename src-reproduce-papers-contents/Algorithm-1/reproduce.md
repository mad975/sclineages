# Step2.py Script

## Overview

`step2.py` is a Python script designed to scrape similar smart contract data from Etherscan, specifically for Ethereum addresses.

## Main Features

 **Scraping Similar Contracts**: 
   - The script fetches and processes data from Etherscan for smart contracts similar to the provided Ethereum addresses.
   - For each contract, it scrapes detailed information, including similarity levels, and saves it to a CSV file (`similarContracts.csv`).

## Setup and Requirements

1. **Python Version**: Python 3.6+
2. **Required Libraries**:
   - `requests`
   - `beautifulsoup4`
   - `csv`
   - `logging`
   - `time`
   - **OS-specific dependencies**:
     - Windows: `ctypes`
     - Linux: `Xlib`
     - macOS: `Quartz` (Install via `pyobjc-framework-Quartz`)

3. **Additional File Requirement**: 
   - The script relies on the contents of the `Algorithm-1` located in the `src-reproduce-papers-contents/Algorithm-1` directory. This algorithm is necessary for processing and analyzing the similarity of contracts during the scraping process.
   
To install the required Python dependencies, run the following command:

```bash
pip install requests beautifulsoup4 Xlib pyobjc-framework-Quartz
```

## Usage

### Command Line Usage from the sclineages/
```bash
cd src-reproduce-papers-contents/Algorithm-1
```
```bash
python step2.py 
```

## Output
**similarContracts.csv:** This file will contain the scraped data of similar contracts with the following columns:

contractsIn: the contract in the data source
simiContract: The similar contract found on Etherscan.
level: The similarity level between the contracts.
