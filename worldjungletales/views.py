from django.conf import settings
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404, redirect, render

from common.recaptcha import Recaptcha
from worldjungletales.forms import CommentForm, SubscribeForm
from worldjungletales.models import Article, Comment, Topic

UserModel = get_user_model()


def about(request):
    ctx = {}
    topics = Topic.objects.filter(status=1)
    ctx["topics"] = topics
    return render(request, "worldjungletales/blog/about.html", ctx)


def comment(request, article_pk):
    article = get_object_or_404(Article, pk=article_pk)
    topics = Topic.objects.filter(status=1)

    if request.method == "POST":
        recaptcha_response = request.POST.get("g-recaptcha-response")
        r = Recaptcha()
        result = r.verify(recaptcha_response)

        if not result:
            return redirect("article", slug=article.slug)

        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.article = article
            comment.save()
            return redirect("article", slug=article.slug)
    else:
        form = CommentForm()

    context = {
        "article": article,
        "topics": topics,
        "form": form,
        "RECAPTCHA_SITE_KEY": settings.RECAPTCHA_SITE_KEY,
    }

    return render(request, "worldjungletales/blog/article.html", context)


def subscribe(request):
    if request.method == "POST":
        form = SubscribeForm(request.POST)

        if form.is_valid():
            form.save()
            topics = Topic.objects.filter(status=1)
            context = {}
            context["message"] = "You have now part of the Scratch family, Thank you!"
            context["topics"] = topics
            return render(request, "worldjungletales/blog/home.html", context)

        else:
            form = SubscribeForm()

    return render(request, "worldjungletales/blog/home.html")


def terms(request):
    topics = Topic.objects.filter(status=1)
    return render(request, "worldjungletales/blog/terms.html", {"topics": topics})


def error_404(request, exception):
    topics = Topic.objects.filter(status=1)
    return render(request, "worldjungletales/blog/404.html", {"topics": topics})


def error_500(request):
    topics = Topic.objects.filter(status=1)
    return render(request, "worldjungletales/blog/500.html", {"topics": topics})


def home(request):
    topics = Topic.objects.filter(status=1)
    articles = Article.objects.filter(status=1).order_by("-updated_on")
    context = {}
    context["topics"] = topics
    context["articles"] = articles

    return render(request, "worldjungletales/blog/home.html", context)


def topics(request, slug):
    topics = Topic.objects.filter(status=1)
    topic = get_object_or_404(Topic, slug=slug)
    articles = Article.objects.filter(topic=topic, status=1).order_by("-updated_on")

    return render(
        request,
        "worldjungletales/blog/articles.html",
        {"articles": articles, "topics": topics},
    )


def article(request, slug):
    article = get_object_or_404(Article, slug=slug)
    topics = Topic.objects.filter(status=1)
    comments = Comment.objects.filter(article=article).all()
    recent = Article.objects.filter(status=1)[:4]

    context = {}
    context["article"] = article
    context["topics"] = topics
    context["comments"] = comments
    context["recents"] = recent
    context["RECAPTCHA_SITE_KEY"] = settings.RECAPTCHA_SITE_KEY
    return render(
        request,
        "worldjungletales/blog/article.html",
        context,
    )
