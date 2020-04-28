from django.db import models


class Article(models.Model):
    title = models.CharField(max_length=200)

    text = models.TextField()
    preview_text = models.TextField(max_length=500)

    icon = models.ImageField(upload_to="icons", blank=True, null=True)

    category = models.ManyToManyField("Category")

    previous_article = models.ForeignKey("self", on_delete=models.SET_NULL, blank=True, null=True, related_name="Article.previous_article+")
    next_article = models.ForeignKey("self", on_delete=models.SET_NULL, blank=True, null=True, related_name="Article.next_article+")

    published = models.BooleanField(default=False)

    upload_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Category(models.Model):
    name = models.CharField(max_length=200)

    icon = models.ImageField(upload_to="icons", blank=True, null=True)
    description = models.TextField(default='')

    def __str__(self):
        return self.name
