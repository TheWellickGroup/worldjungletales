from django.contrib import admin

from worldjungletales.models import Article, Comment, Subscriber, Topic


class ArticleAdmin(admin.ModelAdmin):
    list_display = ("title", "slug", "status", "created_on")
    list_filter = ("status", "topic")
    search_fields = ["title", "content"]
    prepopulated_fields = {"slug": ("title",)}


class TopicAdmin(admin.ModelAdmin):
    list_display = ("title", "slug", "status", "created_on")
    list_filter = ("status",)
    search_fields = ["title", "content"]
    prepopulated_fields = {"slug": ("title",)}


admin.site.register(Article, ArticleAdmin)
admin.site.register(Topic, TopicAdmin)
admin.site.register(Comment)
admin.site.register(Subscriber)
