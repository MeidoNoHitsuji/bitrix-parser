from copy import copy
import json
import os
import re
import uuid
import configs
from configs import StaticType
from typing import Dict, List, Optional, Union
import requests
import bs4
from bs4 import BeautifulSoup
from slugify import slugify

skip_list = ["/news-archive/", "/about_the_university/news", "upravlenie/educational-methodical-management/schedule",
    "media-tsu/videogallery/", "?pagen_1=", "uscience/certification", "uscience/equipment"
    "/uscience/scientific-library/news", "/uscience/scientific-library/question-ans", "uscience/lab",
    "uscience/scientific-innovative-activity/patents", "uscience/scientific-innovative-activity/computer-programs",
    "uscience/scientific-innovative-activity/trademarks"]

doc_mask = (".pdf", ".docs", ".docx", ".doc", ".pptx", ".xlsx", ".rar", ".zip", ".png", ".jpeg", ".jpg", ".xls", ".rtf", ".sig")

def find_urls(tag: bs4.element.Tag):
    urls = list()
    for item in tag.find_all("a"):
        item: bs4.element.Tag = item
        href = item.attrs.get('href')
        if href is None:
            continue
        _href = copy(href)
        href = href.lower()
        
        if "mailto:" in href:
            continue
        
        if any([s in href for s in skip_list]):
            continue
        
        if href.startswith(('http://', 'https://')):
            if "www.tltsu.ru" not in href or "tltsu.ru" not in href:
                continue
        elif "uscience/services" in href:
            href_list = href.replace("https://", '')\
                            .replace("http://", '')\
                            .replace("www.tltsu.ru/", '')\
                            .replace("tltsu.ru/", '')\
                            .replace("uscience/services/", '')\
                            .replace("uscience/services", '')\
                            .strip("/")\
                            .split("/")
            try:
                int(href_list[0])
                continue
            except:
                _href = f"https://www.tltsu.ru/{_href}"
        else:
            _href = f"https://www.tltsu.ru/{_href}"
            
        if not href.lower().endswith(doc_mask):
            _href = _href.strip("/").rstrip('/index.php')
            urls.append(_href)
            
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
        
        if "mailto:" in href:
            continue
        
        if href.startswith(('http://', 'https://')):
            if "www.tltsu.ru" not in href or "tltsu.ru" not in href:
                continue
        elif any([s in href for s in skip_list]):
            continue
        else:
            _href = _href.strip("/")
            _href = f"https://www.tltsu.ru/{_href}"
            
        if href.lower().endswith(doc_mask):
            docs.append(_href)
            
    return docs

def save_card(tag: bs4.element.Tag, uuid: str):
    if not os.path.exists(f"{configs.html_path}"):
        os.makedirs(f"{configs.html_path}")
    if not os.path.exists(f"{configs.html_path}/pages"):
        os.makedirs(f"{configs.html_path}/pages")
    f = open(f"{configs.html_path}/pages/{uuid}.html", "w", encoding='utf8')
    f.write(str(tag))
    f.close()

def get_url_childs(tag: bs4.element.Tag, names: List[str] = [], without: List[str] = [], type = None):
    urls = list()
    
    if type == StaticType.USCIENCE:
        items = list()
        for li in tag.find_all("li"):
            if li.get('class') == "current":
                continue
            else:
                items.append(li.find("a"))
    else:
        items = tag.find_all("a", attrs = {"class": "list-group-item"})
    
    for item in items:
        item: bs4.element.Tag = item
        
        if without is not None and len(without) != 0:
            found = False
            for name in without:
                if item.text in name:
                    found = True
            if found:
                continue
        
        if names is not None and len(names) != 0:
            found = False
            for name in names:
                if item.text in name:
                    found = True
            if not found:
                continue
                       
        href = item.attrs.get('href')
        if href is None:
            continue
        _href = copy(href)
        href = href.lower()
        
        if "mailto:" in href:
            continue
        
        if any([s in href for s in skip_list]):
            continue
        
        if href.startswith(('http://', 'https://')):
            if "www.tltsu.ru" not in href or "tltsu.ru" not in href:
                continue

        elif "uscience/services" in href:
            href_list = href.replace("https://", '')\
                            .replace("http://", '')\
                            .replace("www.tltsu.ru/", '')\
                            .replace("tltsu.ru/", '')\
                            .replace("uscience/services/", '')\
                            .replace("uscience/services", '')\
                            .split("/")
            try:
                int(href_list[0])
                continue
            except:
                _href = f"https://www.tltsu.ru/{_href}"
        else:
            _href = _href.strip("/")
            _href = f"https://www.tltsu.ru/{_href}"
            
        if not href.lower().endswith(doc_mask):
            urls.append(_href)
            
    return urls

def load_row(tag: Union[BeautifulSoup, bs4.element.Tag], type: str = None):
    if type is not None:
        if type == StaticType.CONTAINER:
            row = find_container_row(tag)
        elif type == StaticType.JUMBOTRON:
            row = find_jumbotron_row(tag)
        elif type == StaticType.USCIENCE:
            row, type = find_uscience_row(tag)
        else:
            row = None
    else:
        row = find_container_row(tag)
        type = StaticType.CONTAINER
        if row is None:
            row = find_jumbotron_row(tag)
            type = StaticType.JUMBOTRON
        if row is None:
            row, type = find_uscience_row(tag)
        if row is None:
            type = None
            
    return row, type

def add_child(parent: str, child: str):
    for u, data in allUrls.items():
        if data['current'] == parent:
            if "childs" not in allUrls[u]:
                allUrls[u]["childs"] = list()
            allUrls[u]["childs"].append(child)

def load_card(tag: bs4.element.Tag, childs = None, childs_without = None, tag_soup: Optional[BeautifulSoup] = None, allDocs: List[str] = [], allCountUrls = 0, currentCountUrls = 0, current_uuid = None, type = None):
    save_card(tag, current_uuid)
    
    docs: List[str] = find_docs(tag)
    print(f"Найдено {len(docs)} документов")
    allDocs += docs
    
    urls: List[str] = find_urls(tag)
    print(f"Найдено {len(urls)} ссылок")
    allCountUrls += len(urls)
    
    for url in urls:
        currentCountUrls += 1
        if url in allUrls or url in errorUrls:
            print(f"Ссылка {currentCountUrls}/{allCountUrls} пропущена.")
            continue
            
        try:
            blocks = url.split("/")
    
            if len(blocks) > 1:
                if len(blocks[-1]) == 0:
                    b = blocks[-2]
                else:
                    b = blocks[-1]
        
                if b[0] == "#":
                    sharpUrls.append(url)
                    continue
                
            resp = requests.get(url)
            soup = BeautifulSoup(resp.text, 'lxml')
            row, _type = load_row(soup)
            allUrls[url] = {
                "parent": current_uuid,
                "current": str(uuid.uuid4()),
                "title": get_title(soup),
                "slug": None,
                "type": _type
            }
            
            if allUrls[url]['title'] is not None:
                allUrls[url]['slug'] = slugify(allUrls[url]['title'], separator="_")
        except:
            print(f"Ссылка {currentCountUrls}/{allCountUrls} выдала ошибку.")
            errorUrls.append(url)
            continue
        
        if row is not None:
            print(f"Загружаю ссылку {currentCountUrls}/{allCountUrls}.")
            currentCountUrls, allCountUrls = load_card(row, allDocs=allDocs, tag_soup=soup, currentCountUrls=currentCountUrls, allCountUrls=allCountUrls, current_uuid=allUrls[url]['current'], type=_type)
        else:
            notFoundUrls.append(url)
            del allUrls[url]
            print(f"{url} - не найден")
    print("Все ссылки загружены.")
    
    if (childs is not None and tag_soup is not None) or \
        type is not None and type == StaticType.USCIENCE:
            
        sidebar = find_sidebar(tag_soup, type)
        if sidebar is not None:
            urls = get_url_childs(sidebar, childs, childs_without, type)
            for url in urls:
                if url in allUrls:
                    allUrls[url]["parent"] = current_uuid
                    add_child(current_uuid, allUrls[url]['current'])
                    continue
                
                if url in errorUrls:
                    continue
                
                resp = requests.get(url)
                soup = BeautifulSoup(resp.text, 'lxml')
                row, type = load_row(soup)
                allUrls[url] = {
                    "parent": current_uuid,
                    "current": str(uuid.uuid4()),
                    "title": get_title(soup),
                    "slug": None
                }
                if allUrls[url]['title'] is not None:
                    allUrls[url]['slug'] = slugify(allUrls[url]['title'], separator="_")   
                        
                add_child(current_uuid, allUrls[url]['current'])
                
                if row is not None:
                    currentCountUrls, allCountUrls = load_card(row, allDocs=allDocs, tag_soup=soup, currentCountUrls=currentCountUrls, allCountUrls=allCountUrls, current_uuid=allUrls[url]['current'])
                else:
                    notFoundUrls.append(url)
                    del allUrls[url]
                    print(f"{url} - не найден")
    
    return currentCountUrls, allCountUrls

def get_title(soup: BeautifulSoup):
    head = soup.find("head")
    if head is not None:
        title = head.find("title")
        if title is not None:
            return title.text
    return None
        
def find_sidebar(soup: BeautifulSoup, type = None):
    if type == StaticType.USCIENCE:
        nav = soup.find("div", attrs={"class": "sidebar-nav"})
        if nav is not None:
            ul = nav.find("ul")
            if ul is not None:
                return ul
    
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

def find_uscience_row(soup: BeautifulSoup) -> Optional[bs4.element.Tag]:
    for t in soup.find_all("div", attrs = {"class": "white-box"}):
        content = t.find("div", attrs = {"class": "content"})
        if content is not None:
            return content, StaticType.USCIENCE
    
    for t in soup.find_all("div", attrs = {"class": "content"}):
        content = t.find("div", attrs = {"class": "content"})
        if content is not None:
            row = content.find("div", attrs = {"class": "row"})
            if row is not None:
                boxs = row.find_all("div", attrs={"class": "white-box"})
                if len(boxs) > 0:
                   return content, StaticType.USCIENCE_ROWS
            showcases = content.find_all("ul", attrs={"class": "showcase"})
            if len(showcases) > 0:
                return content, StaticType.USCIENCE_SHOWCASES
               
     
        
    return None, None

def find_jumbotron_row(soup: BeautifulSoup) -> Optional[bs4.element.Tag]:
    for t in soup.find_all("div", attrs = {"class": "jumbotron"}):
        for row in t.find_all("div", attrs = {"class": "row"}):
            _col: bs4.element.Tag = row.find("div", attrs = {"class": "card-body"})
            if _col is not None:
                for s in _col.select("style"):
                    s.extract()
                return _col   
    return None

if __name__ == "__main__":
    allDocs: List[str] = list()
    allUrls: Dict = dict()
    errorUrls: List[str] = list()
    notFoundUrls: List[str] = list()
    sharpUrls: List[str] = list()

    f = open("./urls.json", "r", encoding="utf_8")
    urls: List[dict] = json.loads(f.read())

    for data in urls:            
        allUrls[data['url']] = {
            "current": str(uuid.uuid4()),
            "parent": None,
            "title": data['title'],
            "slug": slugify(data['title'], separator="_") if data['title'] is not None else None,
            "type": data['type']
        }

    for data in urls:
        url: str = data['url']
        type: str = data['type']
        parameters: Optional[List[str]] = data.get('parameters')
        
        if parameters and 'childs' in parameters:
            childs = data.get('childs', [])
            childs_without = data.get('childs_without', [])
        else:
            childs = None
            childs_without = None
            
        try:
            resp = requests.get(url)
            soup = BeautifulSoup(resp.text, 'lxml')
        except:
            del allUrls[url]
            errorUrls.append(url)
            continue   
            
        row, type = load_row(soup, type)

        if row is not None and type is not None:
            print(f"{url} - Начало загрузки")
            load_card(row, childs=childs, childs_without=childs_without, tag_soup=soup, allDocs=allDocs, current_uuid=allUrls[url]['current'])
        else:
            print(f"{url} - не найден")
    
    print(f"НАЧИНАЮ ЗАГРУЖАТЬ НАУЧНЫЙ БЛОК")
    
    resp = requests.get("https://www.tltsu.ru/uscience")
    soup = BeautifulSoup(resp.text, 'lxml')
    
    no_titles = ["главная", "контакты", "en"]
    urls = list()
    
    nav = soup.find("div", attrs={"class": "top-nav-block"})        
    nav = nav.find('ul')
    for item in nav.find_all("div", attrs={"class": "item-text"}):
        a_tag = item.find("a")
        if any([title in a_tag.text.lower() for title in no_titles]):
            continue
        urls += find_urls(item)
    
    for url in urls:
        
        if url in allUrls:
            continue
        
        try:
            resp = requests.get(url)
            soup = BeautifulSoup(resp.text, 'lxml')
        except:
            errorUrls.append(url)
            continue  

        row, type = load_row(soup)

        allUrls[url] = {
            "current": str(uuid.uuid4()),
            "parent": None,
            "title": get_title(soup),
            "type": type
        }
        
        if allUrls[url]['title'] is not None:
            allUrls[url]['slug'] = slugify(allUrls[url]['title'], separator="_")   

        if row is not None and type is not None:
            load_card(row, tag_soup=soup, allDocs=allDocs, current_uuid=allUrls[url]['current'], type=type)


    allDocs = list(set(allDocs))
    print(f"Кол-во доков: {len(allDocs)}")
    
    print(f"Кол-во ссылок: {len(allUrls)}")
    
    errorUrls = list(set(errorUrls))
    print(f"Кол-во сломанных ссылок: {len(errorUrls)}")
    
    notFoundUrls = list(set(notFoundUrls))
    print(f"Кол-во не найденных ссылок: {len(notFoundUrls)}")
    
    sharpUrls = list(set(sharpUrls))
    print(f"Кол-во пропущенных ссылок с параметром: {len(sharpUrls)}")
            
    f = open(f"{configs.html_path}/docs.json", "w", encoding='utf8')
    f.write(json.dumps(allDocs, ensure_ascii=False))
    f.close()

    f = open(f"{configs.html_path}/urls.json", "w", encoding='utf8')
    f.write(json.dumps(allUrls, ensure_ascii=False))
    f.close()
    
    f = open(f"{configs.html_path}/error_urls.json", "w", encoding='utf8')
    f.write(json.dumps(errorUrls, ensure_ascii=False))
    f.close()
    
    f = open(f"{configs.html_path}/not_found_urls.json", "w", encoding='utf8')
    f.write(json.dumps(notFoundUrls, ensure_ascii=False))
    f.close()
    
    f = open(f"{configs.html_path}/sharp_urls.json", "w", encoding='utf8')
    f.write(json.dumps(sharpUrls, ensure_ascii=False))
    f.close()
    