from django.shortcuts import render

# Create your views here.
def show_course(request, course_id):
    return render(request, "show_course.html", {})