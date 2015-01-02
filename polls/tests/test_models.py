import datetime

from django.test import TestCase

from courses.models import Course
from polls.models import Question, Choice, Answer, Poll
from students.models import User


class QuestionModelTest(TestCase):
    def setUp(self):
        self.question = Question.objects.create(title='Chicken or Egg?')

    def test_unicode(self):
        self.assertEqual('Chicken or Egg?', str(self.question))


class ChoiceModelTest(TestCase):
    def setUp(self):
        self.question = Question.objects.create(title='Chicken or Egg?')
        self.choice = Choice.objects.create(question=self.question, text='lorem ipsum')

    def test_unicode(self):
        self.assertEqual('lorem ipsum', str(self.choice))


class AnswerModelTest(TestCase):
    def setUp(self):
        self.course = Course.objects.create(
            name='Test Course',
            url='test-course',
            application_until=datetime.datetime.now(),
        )
        self.student_user = User.objects.create_user('ivo_student@gmail.com', '123')
        self.student_user.status = User.STUDENT
        self.student_user.save()

        self.question = Question.objects.create(title='Chicken or Egg?')
        self.choice = Choice.objects.create(question=self.question, text='lorem ipsum')

        self.answer = Answer.objects.create(choice=self.choice, user=self.student_user)

    def test_unicode(self):
        self.assertEqual('lorem ipsum', str(self.answer))


class PollModelTest(TestCase):
    def setUp(self):
        self.student_user = User.objects.create_user('ivo_student@gmail.com', '123')
        self.student_user.status = User.STUDENT
        self.student_user.save()
        self.question = Question.objects.create(title='Chicken or Egg?')
        self.poll = Poll.objects.create(title='Very important!')
        self.poll.question.add(self.question)

    def test_unicode(self):
        self.assertEqual('Very important!', str(self.poll))

    def test_user_has_answered_when_no_answers(self):
        self.assertFalse(self.poll.user_has_answered(self.student_user))

    def test_user_has_answered_when_answered(self):
        choice = Choice.objects.create(question=self.question)
        Answer.objects.create(choice=choice, user=self.student_user)
        self.assertTrue(self.poll.user_has_answered(self.student_user))

    def test_get_question_list(self):
        expected = 'Chicken or Egg?'
        self.assertEqual(expected, self.poll.get_question_list())
