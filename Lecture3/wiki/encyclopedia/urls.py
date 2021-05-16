from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.title, name="title"),
    path("search_error/", views.search, name="search"),
    path("new_page/", views.new_page, name="new_page"),
    path("new_page_add/", views.new_page_add, name="new_page_add"),
    path("new_error/", views.new_error, name="new_error"),
    path("edit/<str:title>", views.edit, name="edit"),
    path("edit_save/", views.edit_save, name="edit_save"),
    path("random_page/", views.random_page, name="random_page")
]
