# urls is used to define URL patterns and most have corresponding functions defined in views.py

from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>/", views.entry_page, name="entry"),
    path('search/', views.search_wiki, name='search'),
    path('create/', views.create_page, name='create'),
    path('wiki/<str:title>/edit/', views.edit_page, name='edit'),
    path('random/', views.random_page, name='random_page'),
    path('api/apod/', views.apod_view, name='apod_view'),
]