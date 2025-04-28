from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils.text import slugify

STATUS = ((0, "Draft"), (1, "Publish"))


class AbstractBaseModel(models.Model):
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        ordering = ["-created_on"]
        abstract = True


class Topic(AbstractBaseModel):
    title = models.CharField(max_length=20, unique=True)
    slug = models.SlugField(max_length=20, unique=True)
    status = models.IntegerField(choices=STATUS, default=0)

    @property
    def article_count(self):
        return Article.objects.filter(topic=self).count()

    def __str__(self):
        return self.title


class Article(AbstractBaseModel):
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    image_url = models.URLField()
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    content = models.TextField()
    status = models.IntegerField(choices=STATUS, default=0)

    @property
    def views_count(self):
        return self.views_data.count()

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            while self.__class__.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("article", args=[str(self.slug)])


class ArticleView(AbstractBaseModel):
    article = models.ForeignKey(
        "Article", on_delete=models.CASCADE, related_name="views_data"
    )
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(null=True, blank=True)
    referrer = models.URLField(null=True, blank=True)
    session_id = models.CharField(max_length=255, null=True, blank=True)
    region = models.CharField(max_length=100, null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)


class Comment(AbstractBaseModel):
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    comment = models.TextField()

    def __str__(self):
        return self.comment


class Subscriber(AbstractBaseModel):
    email = models.EmailField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.email
