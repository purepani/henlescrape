from re import search
from bs4 import BeautifulSoup
import requests
import os
from pathvalidate import sanitize_filename

search_class = "documents-preface-dl-link"
search_strings = {
    "commentaries": "Open Commentary (PDF)",
    "prefaces": "Open Preface (PDF)",
}

# search_string = "Open"
# filename = input("Enter File Name: ")
filename = "Henle.txt"
main_folder = "files"
for folder in search_strings:
  path = f"{main_folder}/{folder}"
  if not os.path.exists(path):
    os.makedirs(path)

with open(filename, "r") as f:
    for line in f:
        print(line)
        page = requests.get(
            line.strip(),
        )
        html = BeautifulSoup(page.text, "html.parser")
        title = sanitize_filename(html.find("title").string)
        tags = html.find_all("a", class_=search_class)

        for tag in tags:
            for folder, search_string in search_strings.items():
                if search_string in tag.strings:
                    r = requests.get(tag["href"])
                    with open(
                        f"{main_folder}/{folder}/{title}_{folder}.pdf", "wb+"
                    ) as g:
                        g.write(r.content)
