from models import Tag


print(Tag.get(Tag.id.in_([1, 2])))