from django import forms
from django.utils.translation import ugettext as _

from pagedown.widgets import PagedownWidget

from .models import User, UserNote, CourseAssignment, Solution, StudentStartedWorkingAt
from courses.models import Partner


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

    def __init__(self, *args, **kwargs):
        self.author = kwargs.pop('author')
        super(AddNote, self).__init__(*args, **kwargs)

    def save(self, *args, **kwargs):
        instance = super(AddNote, self).save(commit=False)
        instance.author = self.author
        instance.save()
        return instance

    class Meta:
        model = UserNote

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
        self.assignment = kwargs.pop('assignment')
        super(GiveFeedbackForm, self).__init__(*args, **kwargs)
        if self.assignment:
            self.fields['partner'].queryset = Partner.objects.exclude(name='Other Company').order_by('name')

    def save(self, *args, **kwargs):
        instance = super(GiveFeedbackForm, self).save(commit=False)
        instance.assignment = self.assignment
        other_company = Partner.objects.get(name='Other Company')

        if not instance.partner and not instance.partner_name:
            return
        elif instance.partner_name:
            instance.partner = other_company
        elif instance.partner:
            instance.partner_name = instance.partner.name
        instance.save()
        return instance

    class Meta:
        model = StudentStartedWorkingAt

        fields = (
            'partner',
            'partner_name'
        )
