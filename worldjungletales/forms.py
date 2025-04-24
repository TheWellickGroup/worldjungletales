from django import forms

from worldjungletales.models import Article, Comment, Subscriber, Topic


class TopicForm:
    class Meta:
        model = Topic
        fields = "title"


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ("title", "topic", "content")


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("comment",)


class SubscribeForm(forms.ModelForm):
    class Meta:
        model = Subscriber
        fields = ("email",)
