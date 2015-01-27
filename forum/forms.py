from django import forms

from tinymce.widgets import TinyMCE
from pagedown.widgets import PagedownWidget

from forum.models import Topic, Comment

EMPTY_COMMENT_ERROR = 'Празни коментари не са позволени'


class AddTopicForm(forms.ModelForm):
    text = forms.CharField(widget=PagedownWidget())

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
        fields = ('title', 'text',)


class AddCommentForm(forms.ModelForm):
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
        fields = ('text',)
        widgets = {
            'text': PagedownWidget()
        }
        error_messages = {
            'text': {'required': EMPTY_COMMENT_ERROR}
        }
