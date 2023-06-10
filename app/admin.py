from django.contrib import admin
from app.models import Article, Comment, Contact, Subscriber, Topic


# Register your models here.


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
admin.site.register(Contact)
