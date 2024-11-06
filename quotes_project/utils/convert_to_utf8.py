from django.conf import settings
import chardet
import json
import os


# This script formats .json file in utf-8

# ?.json - This is any file name ( ? )
file_path = os.path.join(settings.BASE_DIR, ' ', '?.json')

with open('?.json', 'rb') as file:
    raw_data = file.read()
    encoding = chardet.detect(raw_data)['encoding']

with open('?.json', 'r', encoding=encoding) as file:
    data = json.load(file)

with open('?.json', 'w', encoding='utf-8') as file:
    json.dump(data, file, ensure_ascii=False, indent=4)
