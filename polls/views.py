from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse

from models import Question, Choice, Answer, Poll


def results(request, poll_id):
    return HttpResponse("You're looking at the results of poll %s." % poll_id)


def poll(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)
    questions = poll.question.all()

    return render(request, 'poll.html', locals())
