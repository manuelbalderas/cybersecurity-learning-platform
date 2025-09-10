import requests
from bs4 import BeautifulSoup
import json
import csv
from time import sleep

with open('data/nist_rag_dataset_links.json', 'r', encoding='utf-8') as f:
    glossary = json.load(f)

scraped_data = []


'''
for k,v in glossary.items():

    url = v['link']
    response = requests.get(url)
    if response.status_code != 200:
        print('Failed to retrieve page')
        continue

    soup = BeautifulSoup(response.content, 'html.parser')
    def_span = soup.find(id="term-def-text-0")

    definition = def_span.get_text(strip=True) if def_span is not None else v['definition']

    scraped_obj = {
        'term': k,
        'link': v['link'], 
        'definition': definition
    }

    print(scraped_obj)
    scraped_data.append(scraped_obj)
    
    sleep(0.5)

with open('data/nist_scraped_glossary.jsonl', 'w', encoding='utf-8') as f_out:
    for item in scraped_data:
        f_out.write(json.dumps(item, ensure_ascii=False) + "\n")

print("Scraping and saving complete.")
'''

from concurrent.futures import ThreadPoolExecutor, as_completed
import threading

output_file = 'data/nist_scraped_glossary.jsonl'
file_lock = threading.Lock()
MAX_WORKERS=25

def scrape_term(kv):
    k, v = kv
    url = v['link']
    try:
        response = requests.get(url, timeout=10)
        if response.status_code != 200:
            print(f'Failed to retrieve page for {k}')
            return None

        soup = BeautifulSoup(response.content, 'html.parser')
        def_span = soup.find(id="term-def-text-0")
        definition = def_span.get_text(strip=True) if def_span else v['definition']

        scraped_obj = {
            'term': k,
            'link': url,
            'definition': definition
        }

        print(scraped_obj)
        # Polite delay
        sleep(0.5)
        return scraped_obj

    except Exception as e:
        print(f"Error scraping {k}: {e}")
        return None

def main():
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor, open(output_file, 'w', encoding='utf-8') as f_out:
        futures = {executor.submit(scrape_term, item): item[0] for item in glossary.items()}

        for future in as_completed(futures):
            result = future.result()
            if result is not None:
                with file_lock:
                    f_out.write(json.dumps(result, ensure_ascii=False) + "\n")

    print("Scraping and saving complete.")

if __name__ == "__main__":
    main()