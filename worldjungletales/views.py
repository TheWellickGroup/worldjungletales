import requests
from django.conf import settings
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404, redirect, render

from common.recaptcha import Recaptcha
from worldjungletales.forms import CommentForm, SubscribeForm
from worldjungletales.models import Article, ArticleView, Comment, Topic

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
            return redirect("home")

    else:
        form = SubscribeForm()

    return redirect("home")


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
    qs = Article.objects.filter(status=1).order_by("-updated_on")
    if q := request.GET.get("q"):
        qs = qs.filter(title__icontains=q)

    context = {}
    context["topics"] = topics
    context["articles"] = qs[:8]

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


def track_article_view(request, article):
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0]
    else:
        ip = request.META.get("REMOTE_ADDR")

    if not request.session.session_key:
        request.session.save()
    session_id = request.session.session_key

    geo_data = {}
    try:
        response = requests.get(f"https://ipinfo.io/{ip}/json", timeout=3)
        if response.status_code == 200:
            geo_data = response.json()
    except requests.RequestException:
        pass

    ArticleView.objects.create(
        article=article,
        ip_address=ip,
        user_agent=request.META.get("HTTP_USER_AGENT", ""),
        referrer=request.META.get("HTTP_REFERER", ""),
        session_id=session_id,
        region=geo_data.get("region"),
        country=geo_data.get("country"),
        city=geo_data.get("city"),
    )


def article(request, slug):
    article = get_object_or_404(Article, slug=slug)

    # Track views only if the visitor is NOT the article author (admin)
    if not request.user.is_authenticated or request.user != article.author:
        track_article_view(request, article)

    topics = Topic.objects.filter(status=1)
    comments = Comment.objects.filter(article=article)
    recent = Article.objects.filter(status=1).order_by("-created_on")[:4]

    context = {
        "article": article,
        "topics": topics,
        "comments": comments,
        "recents": recent,
        "RECAPTCHA_SITE_KEY": settings.RECAPTCHA_SITE_KEY,
    }

    return render(
        request,
        "worldjungletales/blog/article.html",
        context,
    )
