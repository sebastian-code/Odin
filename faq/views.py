from django.shortcuts import render

from .models import Faq


def show_faqs(request):
    faqs = Faq.objects.all()
    return render(request, 'show_faqs.html', locals())
