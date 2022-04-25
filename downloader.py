import json
import requests
import os

url_path = "https://tltsu.ru/upload/"
path = "./json/documents.json"
save_path = "./files"
f = open(path, "r", encoding="utf_8")
data = json.loads(f.read())
f.close()

data = list(filter(lambda f: '.php' not in f, data))

i = 1
for d in data:
    d: str = d.strip("/")
    file_url = d.split("/")
    pat_dir = f"{save_path}/{'/'.join(file_url[0:len(file_url) - 1])}"
    if not os.path.exists(pat_dir):
        os.makedirs(pat_dir)
    response = requests.get(url_path + d)
    if response.status_code != 200:
        response = requests.get("https://tltsu.ru/" + d)
        
    if response.status_code != 200:    
        print(f"Ошибка: {url_path + d}")
    else:
        with open(f"{save_path}/{d}", "wb") as f:
            f.write(response.content)
        print(f"Сохранён файл: {i}/{len(data)}")
        
    i += 1
