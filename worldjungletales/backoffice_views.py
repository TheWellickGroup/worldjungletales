from allauth.account.decorators import login_required
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404, render

from common.constants import ARTICLE_IMAGES_BUCKET
from common.supabase import upload_to_supabase_bucket
from worldjungletales.models import Article, Topic

from .forms import ArticleForm, TopicForm

UserModel = get_user_model()


@login_required
def backoffice(request):
    context = {}
    articles = Article.objects.all()
    context["articles"] = articles
    return render(request, "worldjungletales/backoffice/dashboard.html", context)


@login_required
def all_topics(request):
    context = {}
    topics = Topic.objects.all()
    context["topics"] = topics
    return render(request, "worldjungletales/backoffice/topics.html", context)


@login_required
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


@login_required
def articles(request):
    topics = Topic.objects.filter(status=1)
    articles = Article.objects.filter(author=request.user, status=1)
    context = {}
    context["articles"] = articles
    context["topics"] = topics

    return render(request, "worldjungletales/backoffice/articles.html", context)


@login_required
def article_new(request):
    context = {}
    topics = Topic.objects.filter(status=1)
    context["topics"] = topics
    context["form"] = ArticleForm()

    if request.method == "POST":
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            article = form.save(commit=False)
            article.author = request.user
            article.slug = article.title.replace(" ", "-")

            if "image" in request.FILES:
                image = request.FILES["image"]
                try:
                    image_url = upload_to_supabase_bucket(ARTICLE_IMAGES_BUCKET, image)
                    article.image_url = image_url
                except Exception as e:
                    messages.warning(
                        request, f"Failed to upload image {image.name}: {str(e)}"
                    )

            article.save()
            messages.success(
                request, "Succcessfuly Posted an article, Head over to publish!"
            )
            return render(
                request, "worldjungletales/backoffice/new_article.html", context
            )
        else:
            context["form"] = ArticleForm()

    return render(request, "worldjungletales/backoffice/new_article.html", context)


@login_required
def article_edit(request, pk):
    context = {}
    topics = Topic.objects.filter(status=1)
    article = get_object_or_404(Article, pk=pk)
    context["article"] = article
    context["topics"] = topics

    if request.method == "POST":
        form = ArticleForm(request.POST, request.FILES, instance=article)
        if form.is_valid():
            article = form.save(commit=False)
            article.author = request.user
            article.slug = article.title.replace(" ", "-")
            article.save()

            pk = article.pk
            messages.success(
                request, "Successfuly edit of an article, Head over to your Articles"
            )
            context["pk"] = pk
            return render(
                request, "worldjungletales/backoffice/edit_article.html", context
            )

    else:
        form = ArticleForm(instance=article)
        context["form"] = form

    return render(request, "worldjungletales/backoffice/edit_article.html", context)


@login_required
def drafts(request):
    author = request.user
    articles = Article.objects.filter(author=author, status=0)
    topics = Topic.objects.filter(status=1)
    context = {}
    context["articles"] = articles
    context["topics"] = topics

    return render(request, "worldjungletales/backoffice/draft_articles.html", context)


@login_required
def draft_publish(request, article_pk):
    author = request.user
    articles = Article.objects.filter(author=author, status=0)
    Article.objects.filter(author=author, pk=article_pk).update(status=1)
    topics = Topic.objects.filter(status=1)
    context = {}
    context["articles"] = articles
    context["topics"] = topics

    return render(request, "worldjungletales/backoffice/draft_articles.html", context)
