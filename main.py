import os
import xml.etree.ElementTree as ET
from typing import Dict, Optional, Union, List

import configs
import tools
from models import Tag, SessionObj
from configs import Teg

path = configs.data_path
files = os.listdir(path)
contents: Dict[str, ET.ElementTree] = dict()
data: Dict[str, Union[Dict, List]] = dict()
documents = list()

for name in files:
    if '.xml' in name:
        contents[name.replace('.xml', '')] = ET.parse(f"{path}/{name}")

for name, content in contents.items():
    root = content.getroot()

    classifier = root.find(Teg.CLASSIFIER)
    catalog = root.find(Teg.CATALOG)
    props = classifier.find(Teg.PROPERTIES)
    groups = classifier.find(Teg.GROUPS)
    goods_data = catalog.find(Teg.GOODS)

    properties = tools.load_properties(props)

    data[name] = {
        "templates": [],
        "properties": properties,
        "groups": tools.load_properties(groups),
        "products": [tools.get_good(good, properties) for good in goods_data]
    }

    for product in data[name]["products"]:
        documents += tools.get_documents_from_dict(product)
        data[name]['templates'] += [t['id'] for t in product['templates']]

    data[name]['templates'] = list(set(data[name]['templates']))

    print(f"Парсинг файла \"{name}\" завершён.")

documents = list(set(documents))
data['documents'] = documents
print(len(documents))

# for name, _ in contents.items():
#     tags = list()
#     for product in data[name]["products"]:
#         tags += product['tags']
#
#     tags = list(set(tags))
#
#     with SessionObj() as session:
#         for tag in tags:
#             session.add(Tag(name=tag))
#         session.commit()


tools.save_json(data)
