from django.urls import path, include
from django.contrib import admin
from . import views  # Ensure views is imported

urlpatterns = [
    path("", views.index, name="index"),
    path('admin/', admin.site.urls),
    path('alltopics/', views.all_topics, name='all_topics'),
    path("wiki/<str:title>/", views.entry_page, name="entry"),
    path('search/', views.search_wiki, name='search'),
    path('create/', views.create_page, name='create'),
    path('wiki/<str:title>/edit/', views.edit_page, name='edit'),
    path('random/', views.random_page, name='random_page'),
    path('api/apod/', views.apod_view, name='apod_view'),
    path('featured/', views.featured_content_view, name='featured_content'),
]
