from django.http import HttpResponseForbidden
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse


from forum.models import Category, Topic, Comment
from forum.forms import AddTopicForm, AddCommentForm


def show_categories(request):
    categories = Category.objects.all()
    return render(request, 'show_categories.html', locals())


def show_category(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    topics = Topic.objects.filter(category=category).select_related('author').order_by('date').reverse()
    for topic in topics:
        topic.comments_count = Comment.objects.filter(topic=topic).count()
    return render(request, 'show_category.html', locals())


def show_topic(request, topic_id):
    current_user = request.user
    topic = get_object_or_404(Topic, pk=topic_id)
    comments = Comment.objects.filter(topic=topic).select_related('author').order_by('id')

    if current_user.is_authenticated():
        data = request.POST or None
        form = AddCommentForm(data, author=request.user, topic=topic)

        if request.method == 'POST':
            if form.is_valid():
                comment = form.save()
                is_new_topic = comments.count() < 2
                if is_new_topic:
                    topic.subscribe(current_user)
                topic.send_mails(comment)
                return redirect('forum:show_topic', topic_id=topic_id)

    return render(request, 'show_topic.html', locals())


@login_required
def unsubscribe(request, topic_id):
    topic = get_object_or_404(Topic, pk=topic_id)
    topic.unsubscribe(request.user)
    return HttpResponse(status=200)


@login_required
def subscribe(request, topic_id):
    topic = get_object_or_404(Topic, pk=topic_id)
    topic.subscribe(request.user)
    return HttpResponse(status=200)


@login_required
def add_topic(request, category_id):
    current_user = request.user
    category = get_object_or_404(Category, pk=category_id)
    data = request.POST or None
    form = AddTopicForm(data, author=current_user, category=category)

    if request.method == 'POST':
        if form.is_valid():
            topic = form.save()
            topic.subscribe(current_user)
            return redirect('forum:show_category', category_id=category_id)

    return render(request, 'add_topic.html', locals())


@login_required
def edit_topic(request, topic_id):
    current_user = request.user
    topic = get_object_or_404(Topic, pk=topic_id)

    if topic.author != request.user:
        return HttpResponseForbidden()
    data = request.POST if request.POST else None
    form = AddTopicForm(data, author=current_user, category=topic.category, instance=topic)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('forum:show_topic', topic_id=topic_id)

    return render(request, 'edit_topic.html', locals())


@login_required
def edit_comment(request, comment_id):
    current_user = request.user
    comment = get_object_or_404(Comment, pk=comment_id)

    if comment.author != current_user:
        return HttpResponseForbidden()

    data = request.POST if request.POST else None
    form = AddCommentForm(data, author=current_user, instance=comment, topic=comment.topic)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('forum:show_topic', topic_id=comment.topic.pk)

    return render(request, 'edit_comment.html', locals())
