import os
import xml.etree.ElementTree as ET
from typing import Dict, Optional, Union, List

import configs
import tools
from datetime import datetime
from models import New, Tag, SessionObj
from configs import Teg

path = configs.data_path
files = os.listdir(path)
contents: Dict[str, ET.ElementTree] = dict()
data: Dict[str, Union[Dict, List]] = dict()
documents = list()

for name in files:
    if '.xml' in name:
        contents[name.replace('.xml', '')] = ET.parse(f"{path}/{name}")

all_templates = list()
all_tags = list()
all_groups = list()
all_properties = list()

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
        "groups": tools.load_groups(groups),
        "products": [tools.get_good(good, properties) for good in goods_data]
    }
    
    data[name]["properties"] = [property for property in properties if property["id"] not in [
        "CML2_ACTIVE", "CML2_CODE", "CML2_SORT",
        "CML2_ACTIVE_FROM", "CML2_ACTIVE_TO",
        "CML2_PREVIEW_TEXT", "CML2_DETAIL_TEXT",
        "CML2_PREVIEW_PICTURE"
    ] and len(property["id"]) > 0]

    i = 1
    for product in data[name]["products"]:
        product["id"] = i
        documents += tools.get_documents_from_dict(product)
        data[name]['templates'] += [t['id'] for t in product['templates']]
        i += 1
        
    # data[name]['templates'] = list(set(data[name]['templates']))

    print(f"Парсинг файла \"{name}\" завершён.")

documents = list(set(documents))
data['documents'] = documents
print(len(documents))

for name, _ in contents.items():
    all_groups += [g['id'] for g in data[name]['groups']]
    all_properties += [p['id'] for p in data[name]['properties']]
    all_templates += data[name]['templates']
    for product in data[name]["products"]:
        all_tags += product['tags']
        
all_tags = [tag for tag in list(set(all_tags)) if len(tag) > 0]

all_tags = dict({
    (all_tags[i], i+1)
    for i in range(len(all_tags))
})
all_groups = [group for group in list(set(all_groups)) if len(group) > 0]
all_templates = [template for template in list(set(all_templates)) if len(template) > 0]

for name, _ in contents.items():
    for product in data[name]["products"]:
        product['tags'] = [all_tags[tag] for tag in product['tags'] if tag in all_tags.keys()]

print(f"Было свойств: {len(all_properties)}")
print(f"Стало свойств: {len(list(set(all_properties)))}")
_a = list()
dublicat = list()
for a in all_properties:
    if a in _a:
        dublicat.append(a)
    elif len(a) != 0:
        _a.append(a)       
print(f"Отличающиеся свойства: {dublicat[0:5]}")

# with SessionObj() as session:
#     for value, key in all_tags.items():
#         session.add(Tag(id=key, name=value))
#     session.commit()
        
with SessionObj() as session:
    for product in data["Новости"]["products"]:
        session.add(New(
            id=product['id'],
            name=product['name'],
            slug=product['slug'],
            preview=product['preview'],
            # preview_image_id=product['preview_image_id'],
            created_at=datetime.now() if product['created_at'] is None else datetime.strptime(product['created_at'], "%Y-%m-%d %H:%M:%S"),
            # tags=product['tags'],
            # templates=product['templates']
        ))
    session.commit()


tools.save_json(data)
