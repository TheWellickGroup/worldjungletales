from django.contrib.auth import get_user_model
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.views.decorators.csrf import csrf_exempt

from worldjungletales.forms import CommentForm, SubscribeForm
from worldjungletales.models import Article, Comment, Topic

UserModel = get_user_model()


def comment(request, article_pk):
    context = {}
    if request.method == "POST":
        article = get_object_or_404(Article, pk=article_pk)
        topics = Topic.objects.filter(status=1)
        context["article"] = article
        context["topics"] = topics

        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.article = article
            comment.save()
            success = "your comment was posted!"

            return render(
                request,
                "worldjungletales/blog/article.html",
                {"article": article, "topics": topics, "success": success},
            )

    else:
        form = CommentForm()
        context["form"] = form

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


@csrf_exempt
def google_one_tap_login(request):
    login_url = request.build_absolute_uri("/accounts/google/login/")
    return HttpResponseRedirect(login_url)


def error_404(request, exception):
    topics = Topic.objects.filter(status=1)
    return render(request, "worldjungletales/blog/404.html", {"topics": topics})


def error_500(request):
    topics = Topic.objects.filter(status=1)
    return render(request, "worldjungletales/blog/500.html", {"topics": topics})


def home(request):
    topics = Topic.objects.filter(status=1)
    articles = Article.objects.filter(status=1)
    latest = Article.objects.filter(status=1)
    recents = Article.objects.filter(status=1)[:2]
    highlights = Article.objects.filter().order_by("created_on")[:1]
    context = {}
    context["topics"] = topics
    context["articles"] = articles
    context["latests"] = latest
    context["recents"] = recents
    context["highlights"] = highlights

    return render(request, "worldjungletales/blog/home.html", context)


def topics(request, slug):
    topics = Topic.objects.filter(status=1)
    topic = get_object_or_404(Topic, slug=slug)
    articles = Article.objects.filter(topic=topic, status=1)

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
    return render(
        request,
        "worldjungletales/blog/article.html",
        context,
    )
