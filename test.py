import re

q = re.findall(r"\/iblock\/[a-zA-Zа-яА-Я0-9 \/]+.[a-z]{2,4}", "a href=\"/upload/iblock/РЕГЛАМЕНТ РАБОТЫ КОНФЕРЕНЦИИ.docx\"\nanons2022_files/iblock/cb8/cb85e547f310ae991e2acdbcd2daabf3.jpg")
print(q)