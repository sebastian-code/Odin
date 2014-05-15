from django.shortcuts import render, get_object_or_404, redirect
from .models import Category, Topic, Comment
from .forms import AddTopicForm, AddCommentForm


def show_categories(request):
    categories = Category.objects.all()

    return render(request, "categories.html", locals())

def show_category(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    topics = Topic.objects.filter(category=category)
    
    return render(request, "show_category.html", locals())
    

def show_topic(request, topic_id):
    topic = get_object_or_404(Topic, pk=topic_id)
    comments = Comment.objects.filter(topic=topic)

    data = request.POST if request.POST else None
    form = AddCommentForm(data, author=request.user, topic=topic)
    
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('forum:show-topic', topic_id=topic_id)

    return render(request, "show_topic.html", locals())

def add_topic(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    data = request.POST if request.POST else None
    form = AddTopicForm(data, author=request.user, category=category)
    
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('forum:show-category', category_id=category_id)

    return render(request, "add_topic.html", locals())