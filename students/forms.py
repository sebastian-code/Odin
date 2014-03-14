from django import forms
from .models import User


class UserEditForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(UserEditForm, self).__init__(*args, **kwargs)

    def save(self, *args, **kwargs):
        instance = super(UserEditForm, self).save(commit=False)
        instance.save(*args, **kwargs)
        self.save_m2m()

    class Meta:
        model = User
        fields = (
            'github_account',
            'linkedin_account',
            'description',
            'avatar',
        )
