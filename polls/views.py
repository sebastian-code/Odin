from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from forms import AddPollAnswerForm
from models import Question, Choice, Answer, Poll


@staff_member_required
def results(request, poll_id):
    return HttpResponse('You\'re looking at the results of poll %s.' % poll_id)


@login_required
def poll(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)
    if poll.is_active is False or poll.user_has_answered(request.user):
        return redirect('students:user_profile')
    data = request.POST if request.POST else None
    form = AddPollAnswerForm(data=data, poll=poll, user=request.user)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('poll:vote_successful')
    return render(request, 'poll.html', locals())


@login_required
def poll_vote_successful(request):
    return render(request, 'poll_vote_successful.html', locals())
