from bson.objectid import ObjectId
from pymongo import MongoClient
import json

def process_quotes():
    client = MongoClient("mongodb://localhost:27017")
    db = client.hw
    authors_collection = db.authors
    quotes_collection = db.quotes

    with open('D:/Пайтон/web_dj_25/quotes_project/utils/quotes.json', 'r', encoding='utf-8') as file:
        quotes_data = json.load(file)

    for quote_data in quotes_data:
        author_name = quote_data.get("author")
        
        author = authors_collection.find_one({"fullname": author_name})
        if not author:
            author_id = authors_collection.insert_one({
                "fullname": author_name,
                "born_date": quote_data.get("born_date"),
                "born_location": quote_data.get("born_location"),
                "description": quote_data.get("description")
            }).inserted_id
        else:
            author_id = author["_id"]

        existing_quote = quotes_collection.find_one({
            "quote": quote_data.get("quote"),
            "author": author_id
        })

        if not existing_quote:
            quotes_collection.insert_one({
                "quote": quote_data.get("quote"),
                "tags": quote_data.get("tags"),
                "author": ObjectId(author_id)
            })
            print(f"Quote added: {quote_data.get('quote')}")
        else:
            print(f"The quote already exists: {quote_data.get('quote')}")

    print("The process of adding quotes is complete..")

process_quotes()

