from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.title, name="art"),
    path("search/", views.search, name="search"),
    path("random/", views.randomSite, name="random"),
    path("new/", views.new, name="new"),
    path("edit/", views.edit, name="edit")
]
