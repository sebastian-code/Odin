from django.shortcuts import render


def show_categories(request):
    print("llqlq")
    return render(request, "categories.html", locals())