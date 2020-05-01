from django.db import models


class ArticleCategory(models.Model):
    article = models.ForeignKey("Article", on_delete=models.CASCADE)
    category = models.ForeignKey("Category", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.article.title} - {self.category.name}"


class Category(models.Model):
    name = models.CharField(max_length=200)

    icon = models.ImageField(upload_to="icons", blank=True, null=True)
    description = models.TextField(default='')

    def __str__(self):
        return self.name


class Article(models.Model):
    title = models.CharField(max_length=200)

    text = models.TextField()
    preview_text = models.TextField(max_length=500)

    icon = models.ImageField(upload_to="icons", blank=True, null=True)

    previous_article = models.ForeignKey("self", on_delete=models.SET_NULL, blank=True, null=True, related_name="Article.previous_article+")
    next_article = models.ForeignKey("self", on_delete=models.SET_NULL, blank=True, null=True, related_name="Article.next_article+")

    published = models.BooleanField(default=False)

    upload_date = models.DateTimeField(auto_now=True)

    @property
    def categories(self):
        return [m.category.id for m in ArticleCategory.objects.filter(article=self)]

    def set_categories(self, category_list: list):
        current_category_list = ArticleCategory.objects.filter(article=self)

        i: ArticleCategory
        for i in current_category_list:
            if i.pk in category_list:
                category_list.remove(i.pk)
            else:
                i.delete()

        for i in category_list:
            if Category.objects.filter(pk=i).exists():
                ArticleCategory.objects.create(
                    article=self,
                    category_id=i
                )

    def save(self, *args, **kwargs):
        self.update_next_and_previous_articles()
        super(Article, self).save(*args, **kwargs)

    def update_next_and_previous_articles(self):
        if self.previous_article is not None:
            self.previous_article.next_article = self

        if self.next_article is not None:
            self.next_article.previous_article = self

    def __str__(self):
        return self.title
