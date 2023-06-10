from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("topics/", views.all_topics, name="all_topics"),
    path("topics/new/", views.topic_new, name="topic_new"),
    path("topics/<slug:slug>/", views.topics, name="topics"),
    path("articles/new/", views.article_new, name="article_new"),
    path("articles", views.articles, name="articles"),
    path("articles/<slug:slug>/", views.article, name="article"),
    path("articles/<int:pk>/edit/", views.article_edit, name="article_edit"),
    path("drafts", views.drafts, name="drafts"),
    path(
        "drafts/<int:article_pk>/",
        views.draft_publish,
        name="draft_publish",
    ),
    path("register/", views.signup, name="register"),
    path("logout/", views.logout_view, name="logout"),
    path("accounts/profile/", views.profile, name="profile"),
    path("subscribe/", views.subscribe, name="subscribe"),
    path("comment/<int:article_pk>/", views.comment, name="comment"),
    path("terms-and-conditions/", views.terms, name="terms"),
    path("activate/<uidb64>/<token>/", views.activate, name="activate"),
    path("contact/", views.contact_view, name="contact"),
    path("dashboard/", views.dashboard, name="dashboard")
]
