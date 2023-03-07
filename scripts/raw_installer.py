import re
import requests
import tqdm

MODLIST_FILE = "MODLIST.md"
MOD_LINKS = []
PATTERN = re.compile('\(([^\)]+)\)')


def parse_modlist():
    with open(MODLIST_FILE, "r") as f:
        for line in f:
            if line.startswith("*"):
                format_mod(line)


def format_mod(mod_line: str):
    match = PATTERN.search(mod_line[2:]).group(1)
    if (match != None):
        print("Found link for mod: " + mod_line[2:] + " at " + match)
        print("Formatting link...")
        formatted = match.replace("files", "download") + "/file"
        MOD_LINKS.append(formatted)
        print("Formatted link: " + formatted)
    else:
        print("Error: Could not find link for mod: " + mod_line[2:])


def download(url: str, file_name: str):
    resp = requests.get(url, stream=True)
    total = int(resp.headers.get('content-length', 0))
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


def download_mods(mod_folder: str):
    for link in MOD_LINKS:
        file_name: str = link.split("/")[-4]
        download(link, mod_folder + file_name + ".jar")
        break


if __name__ == "__main__":
    key: str = "267C6CA3"
    print("Parsing modlist...")
    parse_modlist()
    print(MOD_LINKS)