import os
import xml.etree.ElementTree as ET
from typing import Dict, Optional, Union, List
from sqlalchemy.orm.session import Session
from slugify import slugify

import configs
import tools
from datetime import datetime
from models import FAQ, Activity, Catalog, Certificates, ComputerProgram, Equipment, Group, Image, Laboratory, LibraryNew, New, Patent, Phonebook, ProfkomNew, Services, Tag, SessionObj, Teacher, Template, Property, Trademarks
from configs import Teg

path = configs.data_path
files = os.listdir(path)
contents: Dict[str, ET.ElementTree] = dict()
data: Dict[str, Union[Dict, List]] = dict()

for name in files:
    if '.xml' in name:
        contents[name.replace('.xml', '')] = ET.parse(f"{path}/{name}")
        
all_documents = list()
all_templates = list()
all_tags = list()
all_groups = list()

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
        i += 1
        
        all_documents += tools.get_documents_from_dict(product)
        all_tags += product['tags']
        
        data[name]['templates'] += [t['id'] for t in product['templates']]
        
    all_templates += data[name]['templates']
    all_groups += data[name]['groups']

    print(f"Парсинг файла \"{name}\" завершён.")

tools.save_json(data)

all_documents = list(set(all_documents))
all_documents = tools.list_to_dict(all_documents)

all_tags = [tag for tag in list(set(all_tags)) if len(tag) > 0]
all_tags = tools.list_to_dict(all_tags)

group_names = list()
_all_groups = list()
i = 1
for group in all_groups:
    if len(group['name']) == 0: continue
    if group['name'] not in group_names:
        _all_groups.append({
            "id": i,
            "old_id": [int(group['id'])],
            "name": group['name'],
            "description": group['description'],
            "slug": slugify(group['name'], separator="_")
        })
        group_names.append(group['name'])
        i+=1
    else:
        for g in _all_groups:
            if g['name'] == group['name']:
                g['old_id'].append(int(group['id']))

all_groups = _all_groups
all_templates = [template for template in list(set(all_templates)) if len(template) > 0]

for name, _ in contents.items():
    for product in data[name]["products"]:
        _groups = list()
        for group in product['groups']:
            for g in list(filter(lambda g: int(group) in g['old_id'], all_groups)):
                _groups.append(g['id'])
        product['groups'] = list(set(_groups))
        product['tags'] = list(set([all_tags[tag] for tag in product['tags'] if tag in all_tags.keys()]))
        
        

print(f"Сохраняем теги")
with SessionObj() as session:
    for value, key in all_tags.items():
        session.add(Tag(id=key, name=value))
    session.commit()        
print(f"Теги сохранены")



print(f"Сохраняем файлы")
with SessionObj() as session:
    for value, key in all_documents.items():
        session.add(Image(id=key, path=value))
    session.commit()        
print(f"Файлы сохранены")



print(f"Сохраняем группы")
with SessionObj() as session:
    for group in all_groups:
        session.add(Group(
            id=group['id'],
            name=group['name'],
            slug=group['slug'],
            description=group['description']
        ))
    session.commit()        
print(f"Группы сохранены")

objs = {
    "Анонсы": Activity,
    "Вопрос-ответ": FAQ,
    "Каталог": Catalog,
    "Лабаратории": Laboratory,
    "Новости библиотеки": LibraryNew,
    "Новости профкома": ProfkomNew,
    "Новости": New,
    "Оборудование": Equipment,
    "Патенты": Patent,
    "Преподаватели": Teacher,
    "Программы для ЭВМ": ComputerProgram,
    "Сертификаты": Certificates,
    "Телефонный справочник": Phonebook,
    "Товарные знаки": Trademarks,
    "Услуги": Services,
}

for name, obj in objs.items():
    print(f"Начало сохранения: {name}")
    with SessionObj() as session:
        session: Session = session
        objs = list()
        for product in data[name]["products"]:
            o = obj(
                id=product['id'],
                name=product['name'],
                slug=product['slug'],
                preview=product['preview'],
                created_at=datetime.strptime(product['created_at'], "%Y-%m-%d %H:%M:%S") if product['created_at'] is not None and len(product['created_at']) > 0 else datetime.now(), 
                tags=session.query(Tag).where(Tag.id.in_(product['tags'])).all(),
                templates=[
                    Template(key=template['id'], value=template['value'])
                    for template in product['templates']
                ],
                groups=session.query(Group).where(Group.id.in_(product['groups'])).all(),
                properties=[
                    Property(name=property['name'], value=property['value'])
                    for property in product["properties"]
                ]
            )
            if product['preview_image'] is not None:
                preview_image = Image.first(Image.path==product['preview_image'])
                if preview_image is not None:
                    o.preview_image_id = preview_image.id
            
            if product['image'] is not None:
                image = Image.first(Image.path==product['image'])
                if image is not None:
                    o.image_id = image.id
                    
            objs.append(o)
        session.add_all(objs)
        session.commit()
    print(f"Окончание сохранения: {name}")