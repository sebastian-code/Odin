from django.forms import ModelForm
from .models import Topic

class AddTopicForm(ModelForm):
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
