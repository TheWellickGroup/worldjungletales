from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from worldjungletales.models import Article, Topic


class WorldJungleTalesSiteMap(Sitemap):
    def items(self):
        return Article.objects.all()

    def lastmod(self, obj):
        return obj.updated_on


class TopicSiteMap(Sitemap):
    def items(self):
        return Topic.objects.all()

    def lastmod(self, obj):
        return obj.updated_on


class StaticViewSitemap(Sitemap):
    priority = 0.5
    changefreq = "daily"

    def items(self):
        return ["home", "terms"]

    def location(self, item):
        return reverse(item)
