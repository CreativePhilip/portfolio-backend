from rest_framework import serializers

from api.models import Article


class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = [
            'id',
            'title',
            'text',
            'preview_text',
            'icon',
            'categories',
            'previous_article',
            'next_article',
            'published',
            'upload_date'
        ]
        read_only_fields = ['categories']

    def save(self, **kwargs):
        model: Article = super(ArticleSerializer, self).save(**kwargs)
        model.update_next_and_previous_articles()

        return model


class MiniArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = [
            'id',
            'title'
        ]