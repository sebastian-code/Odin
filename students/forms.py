from django import forms
from django.utils.translation import ugettext as _

from .models import User, UserNote, CourseAssignment, Solution
from courses.models import Partner

from pagedown.widgets import PagedownWidget


class UserEditForm(forms.ModelForm):
    new_password1 = forms.CharField(widget=forms.PasswordInput, required=False)
    new_password2 = forms.CharField(widget=forms.PasswordInput, required=False)
    avatar_clear = forms.BooleanField(required=False)

    def __init__(self, *args, **kwargs):
        super(UserEditForm, self).__init__(*args, **kwargs)

    def save(self, *args, **kwargs):
        instance = super(UserEditForm, self).save(commit=False)
        avatar_clear = self.cleaned_data.get('avatar_clear')
        new_password = self.cleaned_data.get('new_password1')

        if new_password:
            instance.set_password(new_password)

        if avatar_clear:
            instance.avatar = None

        instance.save(*args, **kwargs)
        self.save_m2m()

    def clean(self):
        cleaned_data = super(UserEditForm, self).clean()
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')

        if password1 != password2:
            raise forms.ValidationError(
                _('The two password fields didn\'t match.')
            )

        return cleaned_data

    class Meta:
        model = User
        fields = (
            'github_account',
            'linkedin_account',
            'description',
            'avatar',
            'mac',
        )


class AddNote(forms.ModelForm):
    text = forms.CharField(widget=PagedownWidget())

    def save(self, *args, **kwargs):
        return super(AddNote, self).save()

    class Meta:
        model = UserNote
        exclude = (
            'author',
        )

        fields = (
            'assignment',
            'text',
        )


class VoteForPartner(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.assignment = kwargs.pop('assignment')
        super(VoteForPartner, self).__init__(*args, **kwargs)

        self.fields['favourite_partners'].widget = forms.CheckboxSelectMultiple()
        if self.assignment:
            self.fields['favourite_partners'].queryset = Partner.objects.filter(
                is_active=True,
                course=self.assignment.course)

    class Meta:
        model = CourseAssignment

        fields = (
            'favourite_partners',
            'cv',
        )


class AddSolutionForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(AddSolutionForm, self).__init__(*args, **kwargs)

    def save(self, *args, **kwargs):
        instance = super(AddSolutionForm, self).save(commit=False)
        instance.user = self.user
        instance.save()
        return instance

    class Meta:
        model = Solution

        fields = (
            'task',
            'repo',
        )


class GiveFeedbackForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('assignment')
        super(GiveFeedbackForm, self).__init__(*args, **kwargs)

        # self.fields['after_course_works_at'] = forms.TypedChoiceField()
        if self.user:
            self.fields['after_course_works_at'].queryset = Partner.objects.all()

    class Meta:
        model = CourseAssignment

        fields = (
            'after_course_works_at',
        )
