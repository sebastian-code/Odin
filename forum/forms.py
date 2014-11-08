from django import forms

from tinymce.widgets import TinyMCE

from .models import Topic, Comment


class AddTopicForm(forms.ModelForm):
    text = forms.CharField(widget=TinyMCE(attrs={'cols': 10, 'rows': 10}))

    def __init__(self, *args, **kwargs):
        self.author = kwargs.pop('author')
        self.category = kwargs.pop('category')
        super(AddTopicForm, self).__init__(*args, **kwargs)

    def save(self, *args, **kwargs):
        self.instance.author = self.author
        self.instance.category = self.category
        return super(AddTopicForm, self).save()

    class Meta:
        model = Topic
        exclude = ['author', 'category']


class AddCommentForm(forms.ModelForm):
    text = forms.CharField(widget=TinyMCE(attrs={'cols': 10, 'rows': 10}))

    def __init__(self, *args, **kwargs):
        self.author = kwargs.pop('author')
        self.topic = kwargs.pop('topic')
        super(AddCommentForm, self).__init__(*args, **kwargs)

    def save(self, *args, **kwargs):
        self.instance.author = self.author
        self.instance.topic = self.topic
        return super(AddCommentForm, self).save()

    class Meta:
        model = Comment
        exclude = ['author', 'topic']
