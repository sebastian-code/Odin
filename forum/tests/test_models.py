from django.test import TestCase

from forum.models import Category, Topic
from students.models import User


class CategoryModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(
            title='Test Category',
        )

    def test_string_representation(self):
        self.assertEqual('Test Category', str(self.category))


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

    def test_string_representation(self):
        self.assertEqual('Test Topic', str(self.topic))
