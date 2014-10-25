from django.test import TestCase

from .models import Category, Topic, Comment
from students.models import User


class CategoryModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(
            title='Test Category',
        )

    def test_unicode(self):
        self.assertEqual('Test Category', unicode(self.category))


class TopicModelTest(TestCase):
    def setUp(self):
        self.student_user = User.objects.create_user('ivo_student@gmail.com', '123')
        self.student_user.status = User.STUDENT
        self.student_user.save()
        self.category = Category.objects.create(
            title='Test Category',
        )

        self.topic = Topic.objects.create(
            title='Test Topic',
            author=self.student_user,
            category=self.category,
        )

    def test_unicode(self):
        self.assertEqual('Test Topic', unicode(self.topic))
