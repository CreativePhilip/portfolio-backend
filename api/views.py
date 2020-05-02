import json
from json import JSONDecodeError

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response

from api.models import Article,  Category, ArticleCategory
from api.serializers import ArticleSerializer, CategorySerializer, MiniArticleSerializer


class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend]

    @action(methods=["get"], detail=True)
    def preview_article(self, request: Request, pk=None):
        article = get_object_or_404(self.queryset, pk=pk)
        return Response(data=MiniArticleSerializer(article).data)

    @action(methods=['get'], detail=True, permission_classes=[permissions.IsAuthenticated])
    def all_articles_shortened(self, request: Request, pk=None):
        articles = Article.objects.all()
        if pk != -1:
            articles = articles.exclude(pk=pk)

        return Response(MiniArticleSerializer(articles, many=True).data)

    @action(methods=['get'], detail=True, permission_classes=[permissions.IsAuthenticated])
    def all_articles(self, request: Request, pk=None):
        articles = Article.objects.all()
        if pk != -1:
            articles = articles.exclude(pk=pk)

        return Response(self.serializer_class(articles, many=True, context={'request': request}).data)

    @action(methods=['get'], detail=False, permission_classes=[])
    def published(self, request: Request, pk=None):
        articles = Article.objects.filter(published=True)
        return Response(self.serializer_class(articles, many=True, context={'request': request}).data)

    @action(methods=['get'], detail=True, permission_classes=[])
    def by_category(self, request: Request, pk=None):
        category = get_object_or_404(Category, pk=pk)
        articles = [a.article for a in ArticleCategory.objects.filter(category=category)]

        return Response(self.serializer_class(articles, many=True, context={'request': request}).data)

    @action(methods=['post'], detail=True)
    def edit_categories(self, request: Request, pk=None):
        article = get_object_or_404(Article, pk=pk)
        try:
            article.set_categories(json.loads(request.data["categories"]))
            return Response({"message": "success"}, status=status.HTTP_200_OK)

        except JSONDecodeError:
            return Response({"error": "Invalid_category_list"}, status=status.HTTP_400_BAD_REQUEST)


class CategoriesViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
