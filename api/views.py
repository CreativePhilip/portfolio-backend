from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response

from api.models import Article,  Category
from api.serializers import ArticleSerializer, CategorySerializer, MiniArticleSerializer


class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.filter(published=True)
    serializer_class = ArticleSerializer
    permission_classes = []
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['category']

    @action(methods=["get"], detail=True)
    def preview_article(self, request: Request, pk=None):
        article = get_object_or_404(self.queryset, pk=pk)
        return Response(data=MiniArticleSerializer(article).data)

    @action(methods=["post"], detail=True)
    def set_previous(self, request: Request, pk=None):
        current_article: Article = get_object_or_404(self.queryset, pk=pk)
        previous_article: Article = get_object_or_404(self.queryset, pk=request.data["pk"])

        current_article.previous_article = previous_article
        previous_article.next_article = current_article

        current_article.save()
        previous_article.save()

        return JsonResponse(data={"response": "Success"})

    @action(methods=["post"], detail=True)
    def set_next(self, request: Request, pk=None):
        current_article: Article = get_object_or_404(self.queryset, pk=pk)
        next_article: Article = get_object_or_404(self.queryset, pk=request.data["pk"])

        current_article.next_article = next_article
        next_article.previous_article = current_article

        current_article.save()
        next_article.save()

        return JsonResponse(data={"response": "Success"})


class CategoriesViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
