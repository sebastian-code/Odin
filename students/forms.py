from django import forms
from .models import User, UserNote
from django.utils.translation import ugettext as _


class UserEditForm(forms.ModelForm):
    new_password1 = forms.CharField(widget=forms.PasswordInput, required=False)
    new_password2 = forms.CharField(widget=forms.PasswordInput, required=False)

    def __init__(self, *args, **kwargs):
        super(UserEditForm, self).__init__(*args, **kwargs)

    def save(self, *args, **kwargs):
        instance = super(UserEditForm, self).save(commit=False)

        new_password = self.cleaned_data.get('new_password1')
        if new_password:
            instance.set_password(new_password)

        instance.save(*args, **kwargs)
        self.save_m2m()

    def clean(self):
        cleaned_data = super(UserEditForm, self).clean()
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')

        if password1 != password2:
            raise forms.ValidationError(
                _("The two password fields didn't match.")
            )

        return cleaned_data

    class Meta:
        model = User
        fields = (
            'github_account',
            'linkedin_account',
            'description',
            'avatar',
        )


class AddNote(forms.ModelForm):
    def save(self, *args, **kwargs):
        return super(AddNote, self).save()

    class Meta:
        model = UserNote
        fields = (
            "text",
            "assignment",
        )
