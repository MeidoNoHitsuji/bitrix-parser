from copy import copy
import json
import os
import re
import configs
from configs import StaticType
from typing import Dict, List, Optional, Union
import requests
import bs4
import uuid
from bs4 import BeautifulSoup

def find_urls(tag: bs4.element.Tag, parent_uuid: str):
    urls = dict()
    for item in tag.find_all("a"):
        item: bs4.element.Tag = item
        href = item.attrs.get('href')
        if href is None:
            continue
        _href = copy(href)
        href = href.lower()
        
        if "mailto:" in href:
            continue
        
        if href.startswith(('http://', 'https://')):
            if "www.tltsu.ru" not in href or "tltsu.ru" not in href:
                continue
        elif "/news-archive/" in href:
            continue
        else:
            _href = _href.strip("/")
            _href = f"https://www.tltsu.ru/{_href}"
            
        if not href.lower().endswith((".pdf", ".docs", ".docx", ".doc", ".pptx", ".xlsx", ".rar", ".zip", ".png", ".jpeg", ".jpg", ".xls", ".rtf", ".sig")):
            urls[_href] = {
                "parent": parent_uuid
            }
            
    return urls

def find_docs(tag: Optional[bs4.element.Tag] = None):
    docs = list()
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
        elif "/news-archive/" in href or "/about_the_university/news" in href or "media-tsu/videogallery/" in href or "?PAGEN_1=" in href:
            continue
        else:
            _href = _href.strip("/")
            _href = f"https://www.tltsu.ru/{_href}"
            
        if href.lower().endswith((".pdf", ".docs", ".docx", ".doc", ".pptx", ".xlsx", ".rar", ".zip", ".png", ".jpeg", ".jpg", ".xls", ".rtf", ".sig")):
            docs.append(_href)
            
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
            row = find_container_row(tag)
        elif type == StaticType.JUMBOTRON:
            row = find_jumbotron_row(tag)
        else:
            row = None
    else:
        row = find_container_row(tag)
        if row is None:
            row = find_jumbotron_row(tag)
            
    return row

def load_card(url: str, data = None, childs = None, childs_wthout = None, allUrls: Dict = dict()):
    
    if url in allUrls.keys():
        return None, None

    current_uuid = str(uuid.uuid4())

    try:
        blocks = url.split("/")
    
        if len(blocks) > 1:
            if len(blocks[-1]) == 0:
                b = blocks[-2]
            else:
                b = blocks[-1]
    
            if b[0] == "#":
                sharpUrls.append(url)
                return None, None
        
        if url not in allUrls:
            allUrls[url] = data
            
        allUrls[url]["current"] = current_uuid
        
        resp = requests.get(url)
        soup = BeautifulSoup(resp.text, 'lxml')
        
        row = load_row(soup)
        
        if row is None:
            print(f"{url} - не найден")
            notFoundUrls.append(url)
            return None, None
        else:
            print(f"Загружаю ссылку {url}.")
    except:
        print(f"Ссылка {url} выдала ошибку.")
        errorUrls.append(url)
        return None, None
    
    save_card(row)
    
    docs = find_docs(row)
    print(f"Найдено {len(docs)} документов")
    
    urls = find_urls(row, current_uuid)
    print(f"Найдено {len(urls)} ссылок")
    
    return docs, urls
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
    allUrls: Dict = dict()
    errorUrls: List[str] = list()
    notFoundUrls: List[str] = list()
    sharpUrls: List[str] = list()

    f = open("./urls.json", "r", encoding="utf_8")
    urls: List[dict] = json.loads(f.read())

    needLoad = dict()
    
    for data in urls:
        needLoad[data['url']] = {
            "parent": None
        }
    
    while len(needLoad) != 0:
        _needLoad = copy(needLoad)
        for url, d in needLoad.items():
            docs, _urls = load_card(url, d, allUrls=allUrls)
            del _needLoad[url]
            
            if _urls is not None:
                keys = list(filter(lambda u: u not in allUrls, _urls.keys()))
                _needLoad.update(
                    {k: _urls[k] for k in keys}
                )
            elif url in allUrls:
                del allUrls[url]
            
            if docs is not None:
                allDocs += docs
        print(f"Кол-во необходимых для закрузки страниц: {len(_needLoad)}")
        needLoad = _needLoad
    # for data in urls:
    #     url: str = data['url']
    #     title: str = data['title']
    #     type: str = data['type']
    #     parameters: Optional[List[str]] = data.get('parameters')
        
    #     if parameters and 'childs' in parameters:
    #         childs = data.get('childs', [])
    #         childs_wthout = data.get('childs_wthout', [])
    #     else:
    #         childs = None
    #         childs_wthout = None
    #     try:
    #         resp = requests.get(url)
    #         soup = BeautifulSoup(resp.text, 'lxml')
    #     except:
    #         allUrls.remove(url)
    #         errorUrls.append(url)
    #         continue   
            
    #     if type == StaticType.USCIENCE:
    #         pass
    #     else:
    #         row = load_row(soup, type)

    #     if row is not None:
    #         print(f"{url} - Начало загрузки")
    #         load_card(row, childs=childs, childs_wthout=childs_wthout, soup=soup, allDocs=allDocs)
    #     else:
    #         print(f"{url} - не найден")
    
    allDocs = list(set(allDocs))
    print(f"Кол-во доков: {len(allDocs)}")
    
    # allUrls = list(set(allUrls))
    print(f"Кол-во ссылок: {len(allUrls)}")
    
    errorUrls = list(set(errorUrls))
    print(f"Кол-во сломанных ссылок: {len(errorUrls)}")
    
    notFoundUrls = list(set(notFoundUrls))
    print(f"Кол-во не найденных ссылок: {len(notFoundUrls)}")
    
    sharpUrls = list(set(sharpUrls))
    print(f"Кол-во пропущенных ссылок с параметром: {len(sharpUrls)}")
            
    f = open(f"{configs.html_path}/docs.json", "w", encoding='utf8')
    f.write(str(allDocs))
    f.close()

    f = open(f"{configs.html_path}/urls.json", "w", encoding='utf8')
    f.write(str(allUrls))
    f.close()
    
    f = open(f"{configs.html_path}/error_urls.json", "w", encoding='utf8')
    f.write(str(errorUrls))
    f.close()
    
    f = open(f"{configs.html_path}/not_found_urls.json", "w", encoding='utf8')
    f.write(str(notFoundUrls))
    f.close()
    
    f = open(f"{configs.html_path}/sharp_urls.json", "w", encoding='utf8')
    f.write(str(sharpUrls))
    f.close()
    