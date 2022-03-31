import json
import os
import re
import configs
from configs import StaticType
from typing import Optional
import requests
import bs4
from bs4 import BeautifulSoup

def find_container_row(soup: BeautifulSoup) -> Optional[bs4.element.Tag]:
    for t in soup.find_all("div", attrs = {"class": "container"}):
        for row in t.find_all("div", attrs = {"class": "row"}):
            for col in row.find_all("div", attrs = {"class": "col-lg-8"}):
                _col = col.find("div", attrs = {"class": "card"})
                if _col is not None:
                    return _col   
    return None

def find_jumbotron_row(soup: BeautifulSoup) -> Optional[bs4.element.Tag]:
    for t in soup.find_all("div", attrs = {"class": "jumbotron"}):
        for row in t.find_all("div", attrs = {"class": "row"}):
            _col: bs4.element.Tag = row.find("div", attrs = {"class": "card-body"})
            if _col is not None:
                for s in _col.select("style"):
                    s.extract()
                return _col   
    return None

def save_html(row: bs4.element.Tag, title: str):
    f = open(f"{configs.html_path}/{title}.html", "w", encoding='utf8')
    f.write(str(row))
    f.close()

new_url = list()


f = open("./urls.json", "r", encoding="utf_8")
urls = json.loads(f.read())

# for url in data:
#     url = url.strip("\n")
#     resp = requests.get(url)
#     soup = BeautifulSoup(resp.text, 'lxml')
#     title = soup.find('title')
#     _data = {
#         "url": url,
#         "title": title.text
#     }
    
#     if "https://www.tltsu.ru/uscience" in url:
#         _data['type'] = "uscience"
#     elif find_container_row(soup) is not None:
#         _data['type'] = "container"
#     elif find_jumbotron_row(soup) is not None:
#         _data['type'] = "jumbotron"
#     else:
#         _data['type'] = None
    
#     new_url.append(_data)
    
# f = open(f"./urls.json", "w", encoding='utf8')
# f.write(json.dumps(new_url, ensure_ascii=False))
# f.close()


for data in urls:
    url: str = data['url']
    title: str = data['title']
    type: str = data['type']

    resp = requests.get(url)
    soup = BeautifulSoup(resp.text, 'lxml')

    if type == StaticType.USCIENCE:
        pass
    elif type == StaticType.CONTAINER:
        row = find_container_row(soup)
    elif type == StaticType.JUMBOTRON:
        row = find_jumbotron_row(soup)

    if row:
        save_html(row, title)
        print(f"{url} - Найден")
    else:
        print(f"{url} - Не найден")
    