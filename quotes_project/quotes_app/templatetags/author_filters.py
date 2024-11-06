# quotes_app/templatetags/author_filters.py
from django import template
from bson.objectid import ObjectId
from ..utils import get_mongodb

register = template.Library()

@register.filter(name='author')
def get_author(id_):
    db = get_mongodb()
    author = db.authors.find_one({'_id': ObjectId(id_)})
    return author['fullname'] if author else "Unknown Author"
