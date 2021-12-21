
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("edit/<str:expenseType>", views.edit, name="edit"),
    path("stats/<str:date>", views.stats, name="stats"),
    path("profile", views.profile, name="profile"),
    path("range", views.get_range, name="range")
]
