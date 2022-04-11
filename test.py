from bs4 import BeautifulSoup
import requests

resp = requests.get("https://www.tltsu.ru/uscience")
soup = BeautifulSoup(resp.text, 'lxml')

urls = list()

nav = soup.find("div", attrs={"class": "top-nav-block"})        
nav = nav.find('ul')
for item in nav.find_all("div", attrs={"class": "item-text"}):
    a_tag = item.find("a")
    print(a_tag.get('href'), a_tag.text)