from copy import copy
import json
import os
import re
import configs
from configs import StaticType
from typing import List, Optional, Union
import requests
import bs4
from bs4 import BeautifulSoup

def find_urls(tag: bs4.element.Tag):
    urls = list()
    for item in tag.find_all("a"):
        item: bs4.element.Tag = item
        href = item.attrs.get('href')
        if href is None:
            continue
        _href = copy(href)
        href = href.lower()
        
        if href.startswith(('http://', 'https://')):
            if "www.tltsu.ru" not in href or "tltsu.ru" not in href:
                continue
        else:
            _href = _href.strip("/")
            _href = f"https://www.tltsu.ru/{_href}"
            
        if not href.lower().endswith((".pdf", ".docs", ".doc", ".pptx", ".xlsx", ".rar", ".png", ".jpeg")):
            urls.append(_href)
            
    return urls

def find_docs(tag: bs4.element.Tag):
    docs = list()
    for item in tag.find_all("a"):
        item: bs4.element.Tag = item
        href = item.attrs.get('href')
        _href = copy(href)
        href = href.lower()
        
        if href.startswith(('http://', 'https://')):
            if "www.tltsu.ru" not in href or "tltsu.ru" not in href:
                continue
        else:
            _href = _href.strip("/")
            _href = f"https://www.tltsu.ru/{_href}"
            
        if href.lower().endswith((".pdf", ".docs", ".doc", ".pptx", ".xlsx", ".rar", ".png", ".jpeg")):
            docs.append(urls)
            
    return docs

def save_card(tag: bs4.element.Tag):
    pass

def get_url_childs(tag: bs4.element.Tag, names: List[str] = [], without: List[str] = []):
    urls = list()
    
    for item in tag.find_all("a", attrs = {"class": "list-group-item"}):
        item: bs4.element.Tag = item
        
        if len(without) != 0:
            found = False
            for name in without:
                if item.text in name:
                    found = True
            if found:
                continue
        
        if len(names) != 0:
            found = False
            for name in names:
                if item.text in name:
                    found = True
            if not found:
                continue
                       
        href = item.attrs.get('href')
        if href:
            urls.append(href)
        else:
            print('href not found!')
            
    return urls

def load_row(tag: Union[BeautifulSoup, bs4.element.Tag], type: str = None):
    if type is not None:
        if type == StaticType.CONTAINER:
            row = find_container_row(soup)
        elif type == StaticType.JUMBOTRON:
            row = find_jumbotron_row(soup)
        else:
            row = None
    else:
        row = find_container_row(tag)
        if row in None:
            row = find_jumbotron_row(tag)
            
    return row

def load_card(tag: bs4.element.Tag, childs = None, childs_wthout = None, soup: Optional[BeautifulSoup] = None):
    save_card(tag)
    
    docs = find_docs(tag)
    print(f"Найдено {len(docs)} документов")
    allDocs += docs
    
    urls = find_urls(tag)
    print(f"Найдено {len(urls)} ссылок")
    
    i = 0
    for url in urls:
        i += 1
        if url in allUrls:
            print(f"Ссылка номер {i} пропущена.")
            continue
        else:
            print(f"Загружаю ссылку номер {i}.")
            allUrls.append(url)
        resp = requests.get(url)
        soup = BeautifulSoup(resp.text, 'lxml')
        row = load_row(soup)
        load_card(row)
    print("Все ссылки загружены.")
        
    # if childs is not None and soup is not None:
    #     sidebar = find_sidebar(soup)
    #     if sidebar is not None:
    #         urls = get_url_childs(sidebar, childs, childs_wthout)
    #         for url in urls:
    #             if url in allUrls:
    #                 continue
    #             else:
    #                 allUrls.append(url)
    #             resp = requests.get(url)
    #             soup = BeautifulSoup(resp.text, 'lxml')
    #             row = load_row(soup)
    #             load_card(row)
    #     else:
    #         print('sidebar not found!')
        
def find_sidebar(soup: BeautifulSoup):
    for t in soup.find_all("div", attrs = {"class": "container"}):
        for row in t.find_all("div", attrs = {"class": "row"}):
            for col in row.find_all("div", attrs = {"class": "col-lg-4"}):
                _col = col.find("div", attrs = {"class": "list-group"})
                if _col is not None:
                    return _col
    
    return None

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

if __name__ == "__main__":
    allDocs: List[str] = list()
    allUrls: List[str] = list()

    f = open("./urls.json", "r", encoding="utf_8")
    urls: List[dict] = json.loads(f.read())

    for data in urls:
        allUrls += data['url']

    for data in urls:
        url: str = data['url']
        title: str = data['title']
        type: str = data['type']
        parameters: Optional[List[str]] = data.get('parameters')
        
        if parameters and 'childs' in parameters:
            childs = data.get('childs', [])
            childs_wthout = data.get('childs_wthout', [])
        else:
            childs = None
            childs_wthout = None

        resp = requests.get(url)
        soup = BeautifulSoup(resp.text, 'lxml')

        if type == StaticType.USCIENCE:
            pass
        else:
            row = load_row(soup, type)

        if row:
            print(f"{url} - Начало загрузки")
            load_card(row, childs=childs, childs_wthout=childs_wthout, soup=soup)
            
    f = open(f"{configs.html_path}/docs.json", "w", encoding='utf8')
    f.write(str(allDocs))
    f.close()

    f = open(f"{configs.html_path}/urls.json", "w", encoding='utf8')
    f.write(str(allUrls))
    f.close()
    