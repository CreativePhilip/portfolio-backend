from django.conf.urls import url
from django.urls import include
from rest_framework.routers import DefaultRouter

from api.article import views as article_views
from api.category import views as category_views

router = DefaultRouter()
router.register(r'articles', article_views.ArticleViewSet)
router.register(r'categories', category_views.CategoriesViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
]
