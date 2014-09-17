from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from models import Question, Choice, Answer, Poll
from forms import AddAnswerPollForm


@staff_member_required
def results(request, poll_id):
    return HttpResponse("You're looking at the results of poll %s." % poll_id)


@login_required
def poll(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)
    questions = poll.question.all()

    return render(request, 'poll.html', locals())


@csrf_exempt
@login_required
@require_http_methods(['POST'])
def add_answer(request):
    answer = Answer.objects.filter(
        user=request.user,
        choice=request.POST['choice'],
    ).first()

    if answer:
        form = AddAnswerPollForm(request.POST, instance=answer, user=request.user)
    else:
        form = AddAnswerPollForm(request.POST, user=request.user)

    if form.is_valid():
        form.save()
        return HttpResponse(status=200)

    return HttpResponse(status=422)
