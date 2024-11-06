from pymongo import MongoClient
import json

client = MongoClient("mongodb://localhost")
db = client.hw

with open('D:/Пайтон/web_dj_25/quotes_project/utils/authors.json', 'r', encoding='utf-8') as file:
    authors = json.load(file)

for author in authors:
    existing_author = db.authors.find_one({'fullname': author['fullname']})
    
    if not existing_author:
        db.authors.insert_one({
            'fullname': author['fullname'],
            'born_date': author.get('born_date', ''),
            'born_location': author.get('born_location', ''),
            'description': author.get('description', '')
        })
        print(f"Author added: {author['fullname']}")
    else:
        print(f"Author {author['fullname']} already exists in the database")
