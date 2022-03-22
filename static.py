import re
from typing import Optional
import requests
import bs4
from bs4 import BeautifulSoup

def find_container_row(soup: BeautifulSoup) -> Optional[bs4.element.Tag]:
    for t in soup.find_all("div", attrs = {"class": "container"}):
        t: bs4.element.Tag = t
        t = t.find("div", attrs = {"class": "row"})
        if t is not None:
            return t
    return None

f = open("./text.txt", "r", encoding="utf_8")
data = f.readlines()
for url in data:
    resp = requests.get(url.strip("\n"))
    soup = BeautifulSoup(resp.text, 'lxml')
    row = find_container_row(soup)
    if row:
        print(f"{url} - Найден")
    else:
        print(f"{url} - Не найден")
    