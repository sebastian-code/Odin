from django.http import HttpResponseForbidden
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse


from .models import Category, Topic, Comment
from .forms import AddTopicForm, AddCommentForm
from .helper import send_topic_subscribe_email, subscribe_to_topic


def show_categories(request):
    categories = Category.objects.all()
    return render(request, 'show_categories.html', locals())


def show_category(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    topics = reversed(
        Topic.objects.filter(category=category).prefetch_related('author', 'comment_set'))

    return render(request, 'show_category.html', locals())


def show_topic(request, topic_id):
    topic = get_object_or_404(Topic, pk=topic_id)
    comments = Comment.objects.filter(topic=topic).order_by('id').select_related('author')

    data = request.POST if request.POST else None
    form = AddCommentForm(data, author=request.user, topic=topic)

    if request.method == 'POST' and request.user.is_authenticated():
        if form.is_valid():
            comment = form.save()
            subscribe_to_topic(request.user, topic)
            send_topic_subscribe_email(topic, comment)

            return redirect('forum:show_topic', topic_id=topic_id)

    return render(request, 'show_topic.html', locals())


@login_required
def unsubscribe(request, topic_id):
    topic = get_object_or_404(Topic, pk=topic_id)
    request.user.subscribed_topics.remove(topic)
    request.user.save()
    return HttpResponse(status=200)


@login_required
def subscribe(request, topic_id):
    topic = get_object_or_404(Topic, pk=topic_id)
    request.user.subscribed_topics.add(topic)
    request.user.save()
    return HttpResponse(status=200)


@login_required
def add_topic(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    data = request.POST if request.POST else None
    form = AddTopicForm(data, author=request.user, category=category)

    if request.method == 'POST':
        if form.is_valid():
            topic = form.save()
            subscribe_to_topic(request.user, topic)
            return redirect('forum:show_category', category_id=category_id)

    return render(request, 'add_topic.html', locals())


@login_required
def edit_topic(request, topic_id):
    topic = get_object_or_404(Topic, pk=topic_id)

    if topic.author != request.user:
        return HttpResponseForbidden()
    data = request.POST if request.POST else None
    form = AddTopicForm(data, author=request.user, category=topic.category, instance=topic)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('forum:show_topic', topic_id=topic_id)

    return render(request, 'edit_topic.html', locals())


@login_required
def edit_comment(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)

    if comment.author != request.user:
        return HttpResponseForbidden()

    data = request.POST if request.POST else None
    form = AddCommentForm(data, author=request.user, instance=comment, topic=comment.topic)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('forum:show_topic', topic_id=comment.topic.pk)

    return render(request, 'edit_comment.html', locals())
