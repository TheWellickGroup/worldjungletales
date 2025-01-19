from django.conf import settings
from django.contrib.auth import get_user_model, logout
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, render
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

from app.models import Article, Comment, Subscriber, Topic

from .forms import (ArticleForm, CommentForm, ContactForm, SignUpForm,
                    SubscribeForm, TopicForm)

UserModel = get_user_model()

# Dashboard


def dashboard(request):
    if request.method == "GET":
        context = {}
        articles = Article.objects.filter().order_by("created_on").all()
        context["articles"] = articles
        return render(request, "article/dashboard.html", context)


def all_topics(request):
    if request.method == "GET":
        context = {}
        topics = Topic.objects.filter().order_by("created_on").all()
        context["topics"] = topics
        return render(request, "topic/index.html", context)


def topic_new(request):
    context = {}
    if request.method == "GET":
        return render(request, "topic/create.html")

    if request.method == "POST":
        form = TopicForm(request.data)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.author = request.user
            topic.slug = topic.title.replace(" ", "-")
            topic.save()
            context["success"] = "Topic Created"
            return render(request, "topic/create.html", context)

    else:
        form = TopicForm()
    return render(request, "topic/create.html", {"form": form})


# 404 Page


def error_404(request, exception):
    categories = Topic.objects.filter(status=1)
    return render(request, "writy/404.html", {"categories": categories})


# 500 Page


def error_500(request):
    categories = Topic.objects.filter(status=1)
    return render(request, "writy/500.html", {"categories": categories})


# Home Page


def home(request):
    categories = Topic.objects.filter(status=1)
    articles = Article.objects.filter(status=1)
    latest = Article.objects.filter(status=1).order_by("-created_on")
    recents = Article.objects.filter(status=1).order_by("-created_on")[:2]
    highlights = Article.objects.filter().order_by("created_on")[:1]
    context = {}
    context["categories"] = categories
    context["articles"] = articles
    context["latests"] = latest
    context["recents"] = recents
    context["highlights"] = highlights

    return render(request, "writy/home.html", context)


def topics(request, slug):
    categories = Topic.objects.filter(status=1)
    topic = get_object_or_404(Topic, slug=slug)
    articles = Article.objects.filter(topic=topic, status=1).order_by("-created_on")

    return render(
        request, "writy/articles.html", {"articles": articles, "categories": categories}
    )


# All articles for a given author


def articles(request):
    categories = Topic.objects.filter(status=1)
    author = request.user
    articles = Article.objects.filter(author=author, status=1).order_by("-created_on")

    return render(
        request,
        "article/articles.html",
        {"articles": articles, "categories": categories},
    )


# View a single article.


def article(request, slug):
    article = get_object_or_404(Article, slug=slug)
    categories = Topic.objects.filter(status=1)
    comments = Comment.objects.filter(article=article).order_by("-created_on").all()
    recent = Article.objects.filter(status=1)[:4]

    context = {}
    context["article"] = article
    context["categories"] = categories
    context["comments"] = comments
    context["recents"] = recent
    return render(
        request,
        "writy/article.html",
        context,
    )


# Create a new article.


def article_new(request):

    context = {}
    categories = Topic.objects.filter(status=1)
    context["categories"] = categories

    if request.method == "GET":
        return render(request, "article/new.html", context)

    if request.method == "POST":
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():

            article = form.save(commit=False)
            article.author = request.user
            article.slug = article.title.replace(" ", "-")
            article.save()

            context["success"] = "Succcessfuly Posted an article, Head over to publish!"
            return render(request, "article/new.html", context)

    else:
        form = ArticleForm()
    return render(request, "article/new.html", {"form": form, "categories": categories})


def article_edit(request, pk):

    context = {}
    categories = Topic.objects.filter(status=1)
    article = get_object_or_404(Article, pk=pk)
    context["article"] = article
    context["categories"] = categories

    if request.method == "GET":
        return render(request, "article/edit.html", context)

    if request.method == "POST":

        form = ArticleForm(request.POST, request.FILES, instance=article)

        if form.is_valid():

            article = form.save(commit=False)
            article.author = request.user
            article.slug = article.title.replace(" ", "-")
            article.save()

            pk = article.pk
            context["success"] = (
                "Successfuly edit of an article, Head over to your Articles"
            )
            context["pk"] = pk

            return render(request, "article/edit.html", context)

    else:
        form = ArticleForm(instance=article)

    return render(
        request,
        "article/edit.html",
        {"form": form, "categories": categories, "article": article},
    )


# List of draft Articles.


def drafts(request):
    author = request.user
    articles = Article.objects.filter(author=author, status=0).order_by("-created_on")
    categories = Topic.objects.filter(status=1)

    return render(
        request, "article/drafts.html", {"articles": articles, "categories": categories}
    )


# Publish a draft article.


def draft_publish(request, article_pk):
    author = request.user
    articles = Article.objects.filter(author=author, status=0).order_by("-created_on")
    Article.objects.filter(author=author, pk=article_pk).update(status=1)
    categories = Topic.objects.filter(status=1)

    return render(
        request, "article/drafts.html", {"articles": articles, "categories": categories}
    )


#  Comment on an article.


def comment(request, article_pk):
    if request.method == "POST":
        article = get_object_or_404(Article, pk=article_pk)
        categories = Topic.objects.filter(status=1)

        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.article = article
            comment.save()
            success = "your comment was posted!"

            return render(
                request,
                "writy/article.html",
                {"article": article, "categories": categories, "success": success},
            )

    else:

        form = CommentForm()

    return render(
        request,
        "writy/article.html",
        {"article": article, "categories": categories, "form": form},
    )


# User


def contact_view(request):

    categories = Topic.objects.filter(status=1)

    if request.method == "GET":

        return render(request, "writy/contact.html", {"categories": categories})

    if request.method == "POST":

        form = ContactForm(request.POST)

        if form.is_valid():

            form.save()

            categories = Topic.objects.filter(status=1)
            context = {}
            context["message"] = "We have recieved your message, Thank you!"
            context["categories"] = categories

            return render(request, "writy/home.html", context)

    else:

        form = ContactForm()

    return render(
        request, "writy/contact.html", {"form": form, "categories": categories}
    )


# Subscribe to newsletter


def subscribe(request):

    if request.method == "GET":
        return render(request, "writy/subscribe.html")

    if request.method == "POST":

        form = SubscribeForm(request.POST)

        if form.is_valid():

            form.save()
            categories = Topic.objects.filter(status=1)
            context = {}
            context["message"] = "You have now part of the Scratch family, Thank you!"
            context["categories"] = categories

            return render(request, "writy/home.html", context)

        else:

            form = SubscribeForm()

    return render(request, "writy.subscribe.html", {"form": form})


# Terms of Service.


def terms(request):
    categories = Topic.objects.filter(status=1)
    return render(request, "writy/terms.html", {"categories": categories})


# User Profile.


def profile(request):
    categories = Topic.objects.filter(status=1)
    return render(request, "registration/profile.html", {"categories": categories})


# User Registration.


def signup(request):
    if request.method == "GET":
        return render(request, "registration/signup.html")

    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            mail_subject = "Activate your account."
            mail_subject1 = "Welcome to Scratch!"

            message = render_to_string(
                "registration/activate_email.html",
                {
                    "user": user,
                    "domain": current_site.domain,
                    "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                    "token": default_token_generator.make_token(user),
                },
            )
            message1 = render_to_string(
                "registration/thank_you.html",
                {
                    "user": user,
                },
            )

            to_email = form.cleaned_data.get("email")
            from_email = settings.EMAIL_HOST_USER

            send_mail(
                mail_subject1,
                message1,
                from_email,
                [to_email],
                fail_silently=False,
            )
            send_mail(
                mail_subject,
                message,
                from_email,
                [to_email],
                fail_silently=False,
            )

            context = {}
            context["message"] = (
                "Please confirm your email address to complete the registration"
            )
            return render(request, "registration/confirm_email.html", context)
    else:
        form = SignUpForm()
    return render(request, "registration/signup.html", {"form": form})


# Activate Email


def activate(request, uidb64, token):
    context = {}

    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = UserModel._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()

        context["message"] = (
            "Thank you for your email confirmation. Now you can login your account."
        )
        return render(request, "registration/login.html", context)

    else:

        context["message"] = "Activation Link is Invalid, Sorry!"
        return render(request, "registration/oops.html", context)


# Logout.


def logout_view(request):
    categories = Topic.objects.filter(status=1)
    logout(request)
    # Redirect to a success page.

    return render(request, "registration/logged_out.html", {"categories": categories})
