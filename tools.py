import os
import re
import xml.etree.ElementTree as ET
import json
import configs
from copy import copy
from typing import Dict, Optional, Union, List
from phpserialize import unserialize

from configs import Teg, Property


def load_properties(root: Optional[ET.Element]):
    properties = list()

    if root:
        for prop in root:
            value = prop.findtext(Teg.VALUE_DEFAULT)
            if value is not None:
                value = unserialize(bytes(value, 'utf-8'))
                if isinstance(value, dict):
                    value = {
                        key.decode(): value.decode() if isinstance(value, bytes) else value
                        for key, value in value.items()
                    }
                elif isinstance(value, bool):
                    value = value
                else:
                    value = value.decode("utf-8")
            d = {
                "id": prop.findtext(Teg.ID),
                "name": prop.findtext(Teg.NAME).strip(" "),
                "value": value
            }

            options = prop.find(Teg.VALUE_OPTIONS)

            if options:
                d["enum_value"] = dict([(f.find(Teg.ID).text, f.find(Teg.VALUE).text) for f in options.findall(Teg.VALUE_OPTION)])
                
            properties.append(d)

    return properties


def load_groups(groups: Optional[ET.Element]):
    data = list()

    if groups:
        for group in groups:
            d = {
                "id": group.findtext(Teg.ID),
                "name": group.findtext(Teg.NAME).strip(" "),
                "description": group.findtext(Teg.DESCRIPTION),
                "slug": group.findtext(Teg.SLUG).strip(" "),
            }
            if d["description"] is not None:
                d["description"] = d["description"].strip(" ")
            data.append(d)

    return data


def get_good(good: ET.Element, properties: dict):
    data = {
        "old_id": good.findtext(Teg.ID),
        "name": good.findtext(Teg.NAME).strip(" "),
        "tags": good.findtext(Teg.TAGS, "").split(", "),
        "image": get_document(
            good.findtext(Teg.IMAGE)    
        ),
        "groups": [group.text for group in good.find(Teg.GROUPS)]
    }

    properties_data = good.find(Teg.PROPERTY_VALUES)
    properties_id = list()
    meta_props = list()
    props = list()

    if properties_data:
        for p in properties_data:
            property: dict = copy(get_property(p.findtext(Teg.ID), properties))
            if property['id'] in [
                "CML2_ACTIVE", "CML2_CODE", "CML2_SORT",
                "CML2_ACTIVE_FROM", "CML2_ACTIVE_TO",
                "CML2_PREVIEW_TEXT", "CML2_DETAIL_TEXT",
                "CML2_PREVIEW_PICTURE"
            ]:
                if "enum_value" in property:
                    value = p.findtext(Teg.VALUE)
                    if value is None:
                        property['value'] = property['value'] if property['value'] is None else property["enum_value"][property['value']]
                    else:
                        property['value'] = property["enum_value"][value]
                else:
                    property['value'] = p.findtext(Teg.VALUE, property['value'])
                
                meta_props.append({
                    "id": property['id'],
                    "name": property['name'],
                    "value": property['value'],
                })
                continue
            else:
                try:
                    int(property['id'])
                except:
                    print(f"Исключающее свойство: {property['id']}")
                    continue   
            property['value'] = p.findtext(Teg.VALUE, property['value'])
            properties_id.append(property['id'])
            props.append({
                "id": int(property['id']),
                "name": property['name'],
                "value": property['value'],
            })

    data['created_at'] = get_property(Property.CREATED_AT, meta_props, 'value')
    data['unpublish_at'] = get_property(Property.UNPUBLISH_AT, meta_props, 'value')
    data['slug'] = get_property(Property.SLUG, meta_props, 'value')
    data['preview'] = get_property(Property.PREVIEW, meta_props, 'value')
    data['preview_image'] = get_document(
        get_property(Property.PREVIEW_IMAGE, meta_props, 'value')
    )
    data['description'] = get_property(Property.DESCRIPTION, meta_props, 'value')

    data['properties_id'] = properties_id
    data['properties'] = props

    data['templates'] = list()

    templates = good.find(Teg.TEMPLATES)
    if templates is not None:
        for template in templates:
            data['templates'].append({
                "id": template.findtext(Teg.ID),
                "value": template.findtext(Teg.VALUE),
            })

    return data


def get_property(id: str, properties: Union[dict, list], key: str = None):
    data = list(filter(lambda p: p["id"] == id, properties))
    if len(data) > 0:
        if key is not None:
            return data[0][key]
        else:
            return data[0]
    else:
        return None


def save_json(data: dict):
    if not os.path.exists(f"{configs.json_path}"):
        os.makedirs(f"{configs.json_path}")
    for name, content in data.items():
        # codecs.open(f"{configs.json_path}/{name}.json", "w", "utf_8")
        f = open(f"{configs.json_path}/{name}.json", "w", encoding='utf8')
        f.write(json.dumps(content, ensure_ascii=False))
        f.close()

def get_document(data: Optional[str]) -> Optional[str]:
    if data is None: return None
    result = get_documents(data)
    if len(result) > 0:
        return result[0]
    else:
        return None

def get_documents(data: str) -> List:
    if data is not None:
        docs =  re.findall(r"\/iblock\/[a-zA-Zа-яА-Я0-9_\- \/]+\.[a-zA-Z]{2,4}|\/medialibrary\/[a-zA-Zа-яА-Я0-9_\- \/]+\.[a-zA-Z]{2,4}|\/uscience\/[a-zA-Zа-яА-Я0-9_\- \/]+\.[a-zA-Z]{2,4}", data)
        return list(filter(lambda d: '.php' not in d, docs))
    else:
        return []


def get_documents_from_dict(data: dict) -> List:
    documents = list()

    for _, v in data.items():
        if isinstance(v, str):
            documents += get_documents(v)
        elif isinstance(v, dict):
            documents += get_documents_from_dict(v)

    return documents

def fix_documents_from_dict(data: dict):    
    for k, v in copy(data).items():
        if isinstance(v, str):
            data[k] = v.replace('"/uscience', '"/upload/uscience').replace('tltsu.ru/uscience', 'tltsu.ru/upload/uscience')
        elif isinstance(v, dict):
            data[k] = fix_documents_from_dict(v)

    return data

def list_to_dict(l: List) -> Dict:
    return dict({
        (l[i], i+1)
        for i in range(len(l))
    })