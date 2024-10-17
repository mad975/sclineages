import csv
import requests
from time import sleep
from bs4 import BeautifulSoup as bs
import logging
import os
import platform
import sys




logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

#config = configparser.ConfigParser()
#config_file_path = 'config.ini'  # Path to your config file
#config.read(config_file_path)

#API_KEY = config['settings'].get('API_KEY', None)
API_KEY = os.getenv('API_KEY')
if not API_KEY:
    logging.error("API_KEY not found in environment variables. Please set it using:\n"
                  "export API_KEY='your_api_key_here' (Linux/MacOS) or\n"
                  "setx API_KEY='your_api_key_here' (Windows)")
    sys.exit(1)


#if not API_KEY:
   # logging.error("API_KEY not found in config.ini. Please add your API key in the following format:\n"
                 # "[settings]\n"
                 # "API_KEY = your_api_key_here\n"
                  #)
    #sys.exit(1)


session = requests.Session()
session.max_redirects = 100

csvData = []
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
}
script_directory = os.path.dirname(__file__)

progress_file = os.path.join(script_directory, 'progress.txt')
failed_urls_file = os.path.join(script_directory, 'failed_urls.txt')
output_file = os.path.join(script_directory, 'similarContracts.csv')
last_contract_file = os.path.join(script_directory, 'last_contract.txt')


def load_last_contract():
    if os.path.exists(last_contract_file):
        with open(last_contract_file, 'r') as f:
            logging.info(f"exist contract saved as last_contract")
            return f.read().strip()
    logging.info(f"the file does'nt exist yet  last_contract_file")
    return None

def save_last_contract(contract):
    with open(last_contract_file, 'w') as f:
        f.write(contract)
    logging.info(f"Last contract saved: {contract}")
    
def get_num_pages(contractAdd):
    url = f"https://etherscan.io/find-similar-contracts?a={contractAdd}&mt=1&m=low&ps=100&p=1"
    logging.info(f"Fetching number of pages from URL: {url}")
    response = session.get(url, headers=headers, allow_redirects=False)
    soup = bs(response.content, 'html.parser')
    num_pages_tag = soup.find('span', {'class': 'page-link text-nowrap'})
    
    if num_pages_tag:
        num_pages_text = num_pages_tag.text.strip()
        num_pages = int(num_pages_text.split("of")[-1].strip())
        logging.info(f"Number of pages found: {num_pages}")
        return num_pages
    else:
        logging.warning("Page text not found, returning None.")
        return None


def save_progress(contract, progress):
    with open(progress_file, 'w') as f:
        f.write(f"{contract},{progress}")
    logging.info(f"Progress saved: {contract} page {progress}")


def load_progress():
    if os.path.exists(progress_file):
        with open(progress_file, 'r') as f:
            contract, progress = f.read().split(',')
            return contract, int(progress)
    return None, 0


def save_failed_url(url):
    with open(failed_urls_file, 'a') as f:
        f.write(url + "\n")
    logging.info(f"Failed URL saved: {url}")


def save_csv_data(data):
    with open(output_file, 'a') as csvfile:
        fieldnames = ['contractsIn', 'simiContract', 'level']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        if csvfile.tell() == 0:  # Check if file is empty
            writer.writeheader()
        writer.writerows(data)

def get_idle_time():
    system = platform.system()
    if system == "Windows":
        return get_idle_time_windows()
    elif system == "Linux":
        return get_idle_time_linux()
    elif system == "Darwin":  # macOS
        return get_idle_time_mac()
    else:
        logging.warning("Idle time check not implemented for this OS")
        return 0  # Default to 0 for unsupported OS

# Windows implementation
def get_idle_time_windows():
    import ctypes
    class LASTINPUTINFO(ctypes.Structure):
        _fields_ = [("cbSize", ctypes.c_uint), ("dwTime", ctypes.c_uint)]

    def get_idle_duration():
        lii = LASTINPUTINFO()
        lii.cbSize = ctypes.sizeof(LASTINPUTINFO)
        if not ctypes.windll.user32.GetLastInputInfo(ctypes.byref(lii)):
            raise ctypes.WinError()
        millis = ctypes.windll.kernel32.GetTickCount() - lii.dwTime
        return millis / 1000.0

    return get_idle_duration()

# Linux implementation
def get_idle_time_linux():
    from Xlib import X, display
    d = display.Display()
    root = d.screen().root
    root.query_pointer()._data
    idle_time = d.get_screen_saver().idle / 1000.0
    d.close()
    return idle_time

# macOS implementation
def get_idle_time_mac():
    from Quartz import CGEventSourceSecondsSinceLastEventType, kCGEventSourceStateHIDSystemState, kCGAnyInputEventType
    idle_time = CGEventSourceSecondsSinceLastEventType(kCGEventSourceStateHIDSystemState, kCGAnyInputEventType)
    return idle_time

def fetch_url(url):
    try:
        response = session.get(url, headers=headers, allow_redirects=False)
        if response.status_code == 200:
            logging.info(f"Successfully fetched URL: {url}")
            return response
    except requests.RequestException as e:
        logging.warning(f"Failed to fetch URL: {url} with error: {e}")
    logging.error(f"Failed to fetch URL: {url}")
    save_failed_url(url)  # Save the URL to the failed list
    return None


API_ENDPOINT = 'https://api.etherscan.io/api'

def get_contract_owner(contract_address, api_key):
    params = {
        'module': 'contract',
        'action': 'getcontractcreation',
        'contractaddresses': contract_address,
        'apikey': api_key
    }
    response = requests.get(API_ENDPOINT, params=params)
    data = response.json()
    if data['status'] == '1' and data['message'] == 'OK':
        return data['result'][0]['contractCreator']
    logging.info(f'Failed to search owner of {contract_address}')
    return None


def same_owner(ownerIn, simContract):
    return ownerIn == get_contract_owner(simContract, API_KEY)
        


def scraper(contractAdd, ownerIn, req_delay=8, idle_threshold=300):
    try:
        numPages = get_num_pages(contractAdd)
    except Exception as e:
        logging.error(f"Failed to get the number of pages for contract {contractAdd}: {e}")
        return
    
    _, start_page = load_progress()
    for i in range(start_page + 1, numPages + 1):
        idle_time = get_idle_time()
        logging.info(f"Idle time: {idle_time} seconds")
        if idle_time > idle_threshold:
            logging.warning(f"System idle time exceeded threshold ({idle_time} seconds). Stopping scraper.")
            save_progress(contractAdd, i - 1)  # Save progress before stopping
            return

        url = f'https://etherscan.io/find-similar-contracts?a={contractAdd}&mt=1&m=low&ps=100&p={i}'
        response = fetch_url(url)
        if response is None:
            continue

        logging.info(f"URL: {url}, Status: {response.status_code}")
        soup = bs(response.content, 'html.parser')
        tds = soup.find_all('td')
        
        local_csv_data = []
        isSimContract = 0
        levelSimilarity = ""
        simContract = ""
        for td in tds:
            inner_text = td.text
            strings = inner_text.split("\n")
            if isSimContract == 2 or (isSimContract >= 8 and (isSimContract - 2) % 6 == 0):
                levelSimilarity = strings[0]
            if isSimContract == 3 or (isSimContract >= 9 and (isSimContract - 3) % 6 == 0):
                simContract = td.a["title"]
                if same_owner(ownerIn, simContract):
                    logging.info(f'Contract: {contractAdd}, Similar Contract: {simContract}, Level: {levelSimilarity}')
                    local_csv_data.append({'contractsIn': contractAdd, 'simiContract': simContract, 'level': levelSimilarity})
        
            isSimContract += 1
        
        csvData.extend(local_csv_data)
        #check same_owner?
         
        save_csv_data(local_csv_data)  
        save_progress(contractAdd, i) 
        sleep(req_delay)


def get_parse_html(file_path, idle_threshold=300):
    delay_seconds = 2
    last_contract = load_last_contract()
    start_reading = last_contract is None
    posiInFile = 0

    with open(file_path) as csvfile:
        reader = csv.DictReader(csvfile, delimiter=',')
        for i, row in enumerate(reader):
            contractAdd = row['contract_address']
            ownerIn = row['owner']
            if not start_reading:
                if contractAdd == last_contract:
                    start_reading = True
                    logging.info(f" We had a last saved contract {contractAdd} at {posiInFile};")
                posiInFile += 1
                logging.info(f" {contractAdd} at {posiInFile} already treated")
                continue

            logging.info(f" {i + 1} In Processing is : {contractAdd} at {posiInFile}")
            save_last_contract(contractAdd)
            try:
                scraper(contractAdd, ownerIn,req_delay=delay_seconds, idle_threshold=idle_threshold)
            except Exception as e:
                logging.error(f"Issue with contract {contractAdd}: {e}")



def delete_intern_files(file_path):
    """Delete a file if it exists."""
    try:
        if os.path.isfile(file_path):
            os.remove(file_path)
            print(f"Deleted file: {file_path}")
        else:
            print(f"No file found at: {file_path}")
    except Exception as e:
        print(f"Error occurred while deleting file: {e}")



if __name__ == "__main__":
  

    file_path = "../../SCLineagesSet/contract-Level/All-contracts-lineages.csv"
    get_parse_html(file_path)
    delete_intern_files(progress_file)
    delete_intern_files(failed_urls_file)
    delete_intern_files(last_contract_file )
    
    print("step2 done ")