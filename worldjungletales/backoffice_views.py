from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import get_object_or_404, redirect, render

from common.supabase import StorageClient
from worldjungletales.models import Article, Topic

from .forms import ArticleForm, TopicForm

UserModel = get_user_model()


@user_passes_test(lambda u: u.is_superuser)
def backoffice(request):
    context = {}
    articles = Article.objects.all()
    context["articles"] = articles
    return render(request, "worldjungletales/backoffice/dashboard.html", context)


@user_passes_test(lambda u: u.is_superuser)
def all_topics(request):
    context = {}
    topics = Topic.objects.all()
    context["topics"] = topics
    return render(request, "worldjungletales/backoffice/topics.html", context)


@user_passes_test(lambda u: u.is_superuser)
def topic_new(request):
    context = {}
    if request.method == "POST":
        form = TopicForm(request.data)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.author = request.user
            topic.slug = topic.title.replace(" ", "-")
            topic.save()
            messages.success(request, "Successfully created a topic")
            return render(
                request, "worldjungletales/backoffice/create_topic.html", context
            )

    else:
        form = TopicForm()
    return render(
        request, "worldjungletales/backoffice/create_topic.html", {"form": form}
    )


@user_passes_test(lambda u: u.is_superuser)
def articles(request):
    topics = Topic.objects.filter(status=1)
    articles = Article.objects.filter(author=request.user, status=1)
    context = {}
    context["articles"] = articles
    context["topics"] = topics

    return render(request, "worldjungletales/backoffice/articles.html", context)


@user_passes_test(lambda u: u.is_superuser)
def article_new(request):
    context = {}
    context["form"] = ArticleForm()

    if request.method == "POST":
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            article = form.save(commit=False)
            article.author = request.user
            s = StorageClient()
            article.image_url = s.upload_article_cover(request)
            article.save()
            messages.success(request, "Succcessfuly Posted an article.")
            return redirect("drafts")
        else:
            context["form"] = form
            messages.error(request, "An error occurred! Please fix the errors below!")

    topics = Topic.objects.filter(status=1)
    context["topics"] = topics
    return render(request, "worldjungletales/backoffice/new_article.html", context)


@user_passes_test(lambda u: u.is_superuser)
def article_edit(request, pk):
    old_article = get_object_or_404(Article, pk=pk, author=request.user)

    if request.method == "POST":
        form = ArticleForm(request.POST, instance=old_article)
        if form.is_valid():
            article = form.save(commit=False)
            article.author = request.user
            s = StorageClient()
            article.image_url = s.upload_article_cover(request, old_article.image_url)
            article.save()
            messages.success(request, "Successfully edited the article!")
            return redirect("drafts")
    else:
        form = ArticleForm(instance=old_article)

    topics = Topic.objects.filter(status=1)
    context = {
        "form": form,
        "article": old_article,
        "topics": topics,
    }
    return render(request, "worldjungletales/backoffice/edit_article.html", context)


@user_passes_test(lambda u: u.is_superuser)
def drafts(request):
    author = request.user
    articles = Article.objects.filter(author=author, status=0)
    topics = Topic.objects.filter(status=1)
    context = {}
    context["articles"] = articles
    context["topics"] = topics

    return render(request, "worldjungletales/backoffice/draft_articles.html", context)


@user_passes_test(lambda u: u.is_superuser)
def draft_publish(request, article_pk):
    author = request.user
    articles = Article.objects.filter(author=author, status=0)
    Article.objects.filter(author=author, pk=article_pk).update(status=1)
    topics = Topic.objects.filter(status=1)
    context = {}
    context["articles"] = articles
    context["topics"] = topics

    return redirect("drafts")
