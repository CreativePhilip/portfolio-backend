from django.contrib import admin

# Register your models here.
from api.models import Article, Category, ArticleCategory

admin.site.register(Article)
admin.site.register(Category)
admin.site.register(ArticleCategory)
