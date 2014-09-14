from django import forms
from django.utils.translation import ugettext as _
from django.core.exceptions import ValidationError

from courses.models import Partner


class SelectPartnerForm(forms.Form):
    CHOICES = ((partner, partner.name) for partner in Partner.objects.filter(is_active=True))
    partners = forms.ChoiceField(choices=CHOICES)


class SelectCompanyForm(forms.Form):
    CHOICES = ((partner, partner.name) for partner in Partner.objects.filter(is_active=False))
    companies = forms.ChoiceField(choices=CHOICES)
