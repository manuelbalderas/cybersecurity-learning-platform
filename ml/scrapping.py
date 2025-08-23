import requests
from bs4 import BeautifulSoup
import csv

url = "https://www.sans.org/security-resources/glossary-of-terms"
response = requests.get(url)
if response.status_code != 200:
    print("Failed to retrieve page")
    exit()

soup = BeautifulSoup(response.content, 'html.parser')
glossary_items = soup.find_all("p")

with open('glossary.csv', 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Term', 'Definition'])

    for item in glossary_items:
        bold = item.find('b')
        if bold:
            term = bold.get_text(strip=True)
            full_text = item.get_text(strip=True)
            definition = full_text.replace(term, '').strip()
            if term and definition:
                writer.writerow([term, definition])