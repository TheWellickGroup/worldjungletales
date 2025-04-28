from django import forms

from worldjungletales.models import Article, Comment, Subscriber, Topic


class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = "__all__"


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ["title", "topic", "content"]


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = "__all__"


class SubscribeForm(forms.ModelForm):
    class Meta:
        model = Subscriber
        fields = "__all__"
