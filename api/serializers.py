from .models import Article, Category
from rest_framework import serializers


class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = [
            'id',
            'title',
            'text',
            'preview_text',
            'icon',
            'category',
            'previous_article',
            'next_article',
            'published',
            'upload_date'
        ]


class MiniArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = [
            'id',
            'title'
        ]


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = [
            'id',
            'name',
            'icon',
            'description'
        ]
