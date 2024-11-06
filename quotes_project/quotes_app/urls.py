from .views import add_author, add_quote, author_list, quote_list
from django.contrib.auth.views import LogoutView
from django.urls import path
from . import views

app_name = "quotes_app"

urlpatterns = [
    path("", views.main, name="root"),
    path("<int:page>/", views.main, name="root_paginate"),
    path("add_author/", add_author, name="add_author"),
    path("add_quote/", add_quote, name="add_quote"),
    path("author_list/", author_list, name="author_list"),
    path("quote_list/", quote_list, name="quote_list"),
    path("tag/<str:tag>/", views.quote_by_tag, name="quote_by_tag"),
    path("author/<str:author_id>/", views.author_detail, name="author_detail"),
    path("delete_author/<str:author_id>/", views.delete_author, name="delete_author"),
    path('login/', views.login_view, name='login'),
    path("register/", views.register_view, name="register"),
    path("logout/", LogoutView.as_view(), name="logout"),
]
