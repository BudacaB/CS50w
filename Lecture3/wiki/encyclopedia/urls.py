from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.title, name="title"),
    path("search_error/", views.search, name="search"),
    path("new_page/", views.new_page, name="new_page"),
    path("new_page_add/", views.new_page_add, name="new_page_add"),
    path("new_error/", views.new_error, name="new_error"),
]
