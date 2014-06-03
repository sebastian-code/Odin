from django.forms import ModelForm
from django import forms
from pagedown.widgets import PagedownWidget
from .models import Topic, Comment

class AddTopicForm(ModelForm):
    text = forms.CharField(widget=PagedownWidget())

    def __init__(self, *args, **kwargs):
        self.author = kwargs.pop('author')
        self.category = kwargs.pop('category')
        super(AddTopicForm, self).__init__(*args, **kwargs)

    def save(self, *args, **kwargs):
        instance = super(AddTopicForm, self).save(commit=False)
        instance.author = self.author
        instance.category = self.category
        instance.save(*args, **kwargs)
        return instance

    class Meta:
        model = Topic
        exclude = ['author', 'category']


class AddCommentForm(ModelForm):
    text = forms.CharField(widget=PagedownWidget())
    
    def __init__(self, *args, **kwargs):
        self.author = kwargs.pop('author')
        self.topic = kwargs.pop('topic')
        super(AddCommentForm, self).__init__(*args, **kwargs)\

    def save(self, *args, **kwargs):
        instance = super(AddCommentForm, self).save(commit=False)
        instance.author = self.author
        instance.topic = self.topic
        instance.save(*args, **kwargs)
        return instance

    class Meta:
        model = Comment
        exclude = ['author', 'topic']