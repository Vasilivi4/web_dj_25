from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django.utils.encoding import force_str
from django.contrib.auth.models import User
from .forms import QuoteForm, AuthorForm
from utils.quotes import process_quotes
from django.contrib import messages
from bson.objectid import ObjectId
from django.core import paginator
from django.conf import settings
from .forms import RegisterForm
from django.urls import reverse
from pymongo import MongoClient
from .utils import get_mongodb
from .models import Quote
import subprocess
import json
import os

def main(request, page=1):
    db = get_mongodb()
    quotes = db.quotes.find()
    par_page = 3
    paginator = Paginator(list(quotes), par_page)
    quotes_on_page = paginator.page(page)
    return render(request, 'quotes_app/index.html', context={'quotes': quotes_on_page})

def add_author(request):
    if request.method == "POST":
        form = AuthorForm(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            cleaned_author_data = cleaned_data.get("fullname")
            form.instance.fullname = cleaned_author_data
            
            try:
                form.save()
                return redirect("quotes_app:author_list")
            except Exception as e:
                import logging
                logger = logging.getLogger(__name__)
                logger.error(f"ќшибка при сохранении автора: {e}")
        else:
            logger.warning(f"ќшибки формы: {form.errors}")

    else:
        form = AuthorForm()

    return render(request, "quotes_app/add_author.html", {"form": form})


def add_quote(request):
    if request.method == "POST":
        form = QuoteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('quotes_app:quote_list')
    else:
        form = QuoteForm()
    return render(request, 'quotes_app/add_quote.html', {'form': form})

def get_mongodb():
    client = MongoClient("mongodb://localhost:27017")
    return client.hw

def author_list(request):
    db = get_mongodb()
    authors = db.authors.find()

    author_data = []
    for author in authors:
        author_dict = dict(author)
        author_dict["author_id"] = str(author["_id"])
        author_data.append(author_dict)

    return render(request, "quotes_app/author_list.html", context={"authors": author_data})



def quote_list(request):
    quotes_file_path = os.path.join(settings.BASE_DIR, 'utils', 'quotes.json')

    try:
        with open(quotes_file_path, 'r', encoding='utf-8') as file:
            quotes = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        quotes = []

    paginator = Paginator(quotes, 3)
    page_number = request.GET.get('page')
    try:
        quotes_page = paginator.page(page_number)
    except PageNotAnInteger:
        quotes_page = paginator.page(1)
    except EmptyPage:
        quotes_page = paginator.page(paginator.num_pages)

    context = {
        'quotes': quotes_page
    }
    return render(request, 'quotes_app/quote_list.html', context)

def quote_by_tag(request, tag):
    quotes_file_path = os.path.join(settings.BASE_DIR, 'utils', 'quotes.json')
    
    try:
        with open(quotes_file_path, 'r', encoding='utf-8') as file:
            quotes = json.load(file)
    except FileNotFoundError:
        quotes = []
    except json.JSONDecodeError:
        quotes = []
    
    filtered_quotes = [quote for quote in quotes if tag in quote.get('tags', [])]
    
    context = {
        'quotes': filtered_quotes,
        'tag': tag
    }
    return render(request, 'quotes_app/quote_list.html', context)



@csrf_exempt
def add_author(request):
    if request.method == "POST":
        fullname = request.POST.get("fullname")
        born_date = request.POST.get("born_date")
        born_location = request.POST.get("born_location")
        description = request.POST.get("description")

        new_author = {
            "fullname": fullname,
            "born_date": born_date,
            "born_location": born_location,
            "description": description
        }

        authors_file_path = os.path.join("utils", "authors.json")

        try:
            with open(authors_file_path, "r", encoding="utf-8") as file:
                authors = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            authors = []

        authors.append(new_author)
        with open(authors_file_path, "w", encoding="utf-8") as file:
            json.dump(authors, file, ensure_ascii=False, indent=4)

        try:
            script_path = os.path.join("utils", "author.py")
            subprocess.run(["python", script_path], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Ошибка при запуске скрипта: {e}")

        return redirect("quotes_app:author_list")

    return render(request, "quotes_app/add_author.html")


@csrf_exempt
def add_quote(request):
    if request.method == "POST":
        quote_text = request.POST.get("quote")
        author = request.POST.get("author")
        tags = request.POST.get("tags").split(",")

        new_quote = {
            "quote": quote_text,
            "tags": [tag.strip() for tag in tags],
            "author": author
        }

        quotes_file_path = os.path.join("utils", "quotes.json")

        try:
            with open(quotes_file_path, "r", encoding="utf-8") as file:
                quotes = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            quotes = []

        quotes.append(new_quote)
        with open(quotes_file_path, "w", encoding="utf-8") as file:
            json.dump(quotes, file, ensure_ascii=False, indent=4)

        process_quotes()

        return redirect("quotes_app:root")

    return render(request, "quotes_app/add_quote.html")

def author_detail(request, author_id):
    db = get_mongodb()

    author = db.authors.find_one({'_id': ObjectId(author_id)})

    if author is None:
        return render(request, 'quotes_app/author_not_found.html', status=404)

    db.quotes_list.delete_many({'author_id': ObjectId(author_id)})

    db.authors.delete_one({'_id': ObjectId(author_id)})

    return redirect('quotes_app:author_list')


def get_mongodb():
    client = MongoClient("mongodb://localhost:27017")
    return client.hw

def delete_author(request, author_id):
    client = MongoClient("mongodb://localhost:27017")
    db = client.hw
    authors_collection = db.authors
    quotes_collection = db.quotes

    authors_collection.delete_one({"_id": ObjectId(author_id)})
    quotes_collection.delete_many({"author": ObjectId(author_id)})

    return redirect('quotes_app:author_list')

def delete_quote(request, quote_id):
    db = get_mongodb()
    db.quotes.delete_one({"_id": ObjectId(quote_id)})
    return redirect("quote_list")

def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('quotes_app:root'))
        else:
            return render(request, 'quotes_app/login.html', {'error': 'Неверные данные'})

    return render(request, 'quotes_app/login.html')


def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, f'Account created for {user.username}!')
            return redirect('quotes_app:login')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = RegisterForm()
    
    return render(request, 'quotes_app/register.html', {'form': form})

