import requests
from bs4 import BeautifulSoup
from tqdm import tqdm

COOKIE = "eyJ0b2tlbiI6IjM5MjQ6TUVVQ0lRRHUzekFXMkFJT0pyNjlvc1d6YWwzSFlDamVuQTc3ajV1eDNrQlRtQm4vcFFJZ1MvcHNsenBEV2NobXhhNEhGbGsvdVAyYU5SR2dENmFMaUFSaHBYN0dpVWc9In0.ZzGHGA.45D1LHepcAEQyW6egVu0HM1jeoo"
base_url = "https://chal01-lx4evlcv.hack-challenge.lug.ustc.edu.cn:8443"
response = requests.get(base_url+"/list", cookies={'session': COOKIE})
print(response.text)
soup = BeautifulSoup(response.text, 'html.parser')

links = soup.find_all('a')

data = []
for link in tqdm(links, desc="Fetching URLs"):
    href = link.get('href')
    if not href.startswith('/view'):
        continue
    text = link.text
    # Fetch content from each URL
    response = requests.get(base_url+href, cookies={'session': COOKIE})
    content = response.text
    
    link_data = {
        'url': href,
        'text': text,
        'content': content
    }
    data.append(link_data)

# Convert to JSON
import json
with open('links_data.json', 'w') as f:
    json.dump(data, f, indent=4)