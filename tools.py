import re
import xml.etree.ElementTree as ET
import json
import configs
from copy import copy
from typing import Optional, Union, List
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
                d["enum_value"] = options.findtext(Teg.VALUE)
            properties.append(d)

    return properties


def load_groups(groups: Optional[ET.Element]):
    data = list()

    if groups:
        for group in groups:
            d = {
                "id": group.findtext(Teg.ID),
                "name": group.findtext(Teg.NAME).strip(" "),
                "description": group.findtext(Teg.DESCRIPTION).strip(" "),
                "slug": group.findtext(Teg.SLUG).strip(" "),
            }
            data.append(d)

    return data


def get_good(good: ET.Element, properties: dict):
    data = {
        "id": good.findtext(Teg.ID),
        "name": good.findtext(Teg.NAME).strip(" "),
        "tags": good.findtext(Teg.TAGS, "").split(", "),
        "image": good.findtext(Teg.IMAGE),
        "groups": [group.findtext(Teg.ID) for group in good.find(Teg.GROUPS)]
    }

    properties_data = good.find(Teg.PROPERTY_VALUES)
    properties_id = list()
    props = list()

    if properties_data:
        for p in properties_data:
            property: dict = copy(get_property(p.findtext(Teg.ID), properties))
            property['value'] = p.findtext(Teg.VALUE, property['value'])
            properties_id.append(property['id'])
            props.append({
                "id": property['id'],
                "name": property['name'],
                "value": property['value'],
            })

    data['properties_id'] = properties_id
    data['properties'] = props

    data['created_at'] = get_property(Property.CREATED_AT, props)
    data['slug'] = get_property(Property.SLUG, props)
    data['preview'] = get_property(Property.PREVIEW, props)
    data['preview_image'] = get_property(Property.PREVIEW_IMAGE, props)
    data['description'] = get_property(Property.DESCRIPTION, props)

    data['templates'] = list()

    templates = good.find(Teg.TEMPLATES)
    if templates is not None:
        for template in templates:
            data['templates'].append({
                "id": template.findtext(Teg.ID),
                "value": template.findtext(Teg.VALUE),
            })

    return data


def get_property(id: str, properties: Union[dict, list]):
    data = list(filter(lambda p: p["id"] == id, properties))
    if len(data) > 0:
        return data[0]
    else:
        return None


def save_json(data: dict):
    for name, content in data.items():
        # codecs.open(f"{configs.json_path}/{name}.json", "w", "utf_8")
        f = open(f"{configs.json_path}/{name}.json", "w", encoding='utf8')
        f.write(json.dumps(content, ensure_ascii=False))
        f.close()


def get_documents(data: str) -> List:
    if data is not None:
        return re.findall(r"\/iblock\/[a-zA-Zа-яА-Я0-9 \/]+.[a-zA-Z]{2,4}", data)
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
