import datetime

from django.test import TestCase
from django.core.urlresolvers import reverse

from models import Question, Choice, Answer, Poll
from courses.models import Course
from students.models import CourseAssignment, User


class PollViewsTest(TestCase):

    def setUp(self):
        self.student_user = User.objects.create_user('ivo_student@gmail.com', '123')
        self.student_user.status = User.STUDENT
        self.student_user.save()
        self.question = Question.objects.create(title='Chicken or Egg?')
        self.poll = Poll.objects.create(title='Very important!')
        self.poll.question.add(self.question)
        self.choice = Choice.objects.create(question=self.question)

    def test_poll_view_get(self):
        self.client.login(username='ivo_student@gmail.com', password='123')
        response = self.client.get(reverse('polls:vote', kwargs={'poll_id': self.poll.id}))
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed('poll.html', response)
