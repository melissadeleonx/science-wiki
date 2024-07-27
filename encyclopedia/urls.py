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
    
    # Add URL patterns for articles
    # path('articles/', views.article_list, name='article-list'),
    # path('science-news/', views.science_news, name='science-news'),

    # path('articles/<int:pk>/', views.article_detail, name='article-detail'),
    # path('articles/create/', views.article_create, name='article-create'),
    # path('articles/<int:pk>/edit/', views.article_edit, name='article-edit'),
    # path('articles/<int:pk>/delete/', views.article_delete, name='article-delete'),
]
