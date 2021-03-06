data_path = "./data"
json_path = "./json"
html_path = "./html"


class Teg:
    CLASSIFIER = "Классификатор"
    CATALOG = "Каталог"
    GOODS = "Товары"
    TAGS = "БитриксТеги"
    PROPERTIES = "Свойства"
    PROPERTY = "Свойство"
    GROUPS = "Группы"
    ID = "Ид"
    SLUG = "БитриксКод"
    NAME = "Наименование"
    DESCRIPTION = "Описание"
    VALUE_OPTIONS = "ВариантыЗначений"
    VALUE = "Значение"
    VALUE_OPTION = "Вариант"
    VALUE_DEFAULT = "БитриксЗначениеПоУмолчанию"
    IMAGE = "Картинка"
    PROPERTY_VALUES = "ЗначенияСвойств"
    PROPERTY_VALUE = "ЗначенияСвойства"
    TEMPLATES = "НаследуемыеШаблоны"
    TEMPLATE = "Шаблон"


class Property:
    CREATED_AT = "CML2_ACTIVE_FROM"
    UNPUBLISH_AT = "CML2_ACTIVE_TO"
    SLUG = "CML2_CODE"
    PREVIEW = "CML2_PREVIEW_TEXT"
    DESCRIPTION = "CML2_DETAIL_TEXT"
    PREVIEW_IMAGE = "CML2_PREVIEW_PICTURE"
    
class StaticType:
    USCIENCE = "uscience"
    USCIENCE_ROWS = "uscience_rows"
    USCIENCE_SHOWCASES = "uscience_showcases"
    CONTAINER = "container"
    ONLY_CONTAINER = "only_container"
    JUMBOTRON = "jumbotron"
