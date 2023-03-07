from typing import Union
import requests
from bs4 import BeautifulSoup as bs
from tqdm import tqdm

API_KEY: str = '267C6CA3'
BASE_LINK: str = 'https://edge.forgecdn.net/files/{id-first}/{id-second}/{file-name}?api-key={API_KEY}'


def _split_id(id: int):
    return (id // 1000, id % 1000)


def _transform_link(mod_link: str):
    soup = bs(requests.get(mod_link).text, 'html.parser')
    file_name = soup.find('div', class_='flex flex-col md:flex-row justify-between border-b border-gray--100 mb-2 pb-4').text
    print(file_name)


def download(url: str, file_name: str):
    resp = requests.get(url, stream=True)
    total = int(resp.headers.get('content-length', 0))
    print(f"Downloading {file_name}... ({total} bytes)")
    with open(file_name, 'wb') as f, tqdm(
        desc=file_name,
        total=total,
        unit='iB',
        unit_scale=True,
        unit_divisor=1024,
    ) as bar:
        for data in resp.iter_content(chunk_size=1024):
            size = f.write(data)
            bar.update(size)


download("https://edge.forgecdn.net/files/3940/240/jei-1.18.2-9.7.1.255.jar?api-key=267C6CA3", "jei.jar")
