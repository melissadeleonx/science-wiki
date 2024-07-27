from django.contrib import admin
from .models import Article


class ArticleAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'published_at')  
    search_fields = ('title', 'content')  
    list_filter = ('published_at',) 

admin.site.register(Article, ArticleAdmin)
