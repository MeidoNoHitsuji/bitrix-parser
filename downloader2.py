import json
import os
import re
from typing import List
import requests

save_path = "./files2"

path = "./html/docs.json"
f = open(path, "r", encoding="utf_8")
data: List[str] = json.loads(f.read())
f.close()

path = "./json/documents.json"
f = open(path, "r", encoding="utf_8")
data2 = json.loads(f.read())
f.close()

reg = r"^(http|https):\/\/([a-z]*\.)*tltsu\.ru/"

_data = dict()

for d in data:
    value = d
    q = re.match(reg, d)
    if q is not None:
        value = d.replace(q.group(), "/") 
    value: str = value.strip("/")
    _data[d] = value.split("/")

_errors = {
    "easy": [],
    "critical": []
}

i = 0
for k, v in _data.items():
    i += 1
    if os.path.exists(f"{save_path}/{'/'.join(v)}"):
        continue
    pat_dir = f"{save_path}/{'/'.join(v[0:len(v) - 1])}"
    if not os.path.exists(pat_dir):
        os.makedirs(pat_dir)
    response = requests.get(k)
        
    if response.status_code != 200:    
        print(f"Ошибка: {k}")
        _errors["easy"].append(k)
    else:
        try:
            with open(f"{save_path}/{'/'.join(v)}", "wb") as f:
                f.write(response.content)
            print(f"Сохранён файл: {i}/{len(data)}")
        except:
            print(f"Критическая ошибка: {k}")
            _errors["critical"].append(k)

print(f"Обычных ошибок: {len(_errors['easy'])}")
print(f"Критических ошибок: {len(_errors['critical'])}")

f = open(f"{save_path}/errors.json", "w", encoding='utf8')
f.write(json.dumps(_errors, ensure_ascii=False))
f.close()