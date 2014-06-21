from django.test import TestCase, client
from django.core.urlresolvers import reverse

from students.models import User
from .models import Category, Topic

class CoursesTest(TestCase):
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

    def test_show_categories_status(self):
        self.client = client.Client()
        response = self.client.get(reverse('forum:forum'))
        self.assertEqual(200, response.status_code)

    def test_show_category_status(self):
        self.client = client.Client()
        response = self.client.get(reverse('forum:show-category', kwargs={'category_id':self.category.id}))
        self.assertEqual(200, response.status_code)

    def test_show_nonexistent_category_status(self):
        self.client = client.Client()
        response = self.client.get(reverse('forum:show-category', kwargs={'category_id':'234'}))
        self.assertEqual(404, response.status_code)

    def test_show_topic_status(self):
        self.client = client.Client()
        response = self.client.get(reverse('forum:show-topic', kwargs={'topic_id':self.topic.id}))
        self.assertEqual(200, response.status_code)

    def test_show_nonexistent_topic_status(self):
        self.client = client.Client()
        response = self.client.get(reverse('forum:show-topic', kwargs={'topic_id':'234'}))
        self.assertEqual(404, response.status_code)

    def test_add_topic_status(self):
        self.client = client.Client()
        self.client.login(username='ivo_student@gmail.com', password='123')
        before_add = Topic.objects.count()
        response = self.client.post(reverse('forum:add-topic',  kwargs={'category_id':self.category.id}), {
            'title': 'My Topic',
            'text': 'Lqlqlq',
            'author': self.student_user,
            'category': self.category,
        })

        after_add = Topic.objects.count()
        self.assertEqual(before_add + 1, after_add)

    def test_add_topic_not_logged_redirect(self):
        self.client = client.Client()
        
        before_add = Topic.objects.count()
        response = self.client.post(reverse('forum:add-topic',  kwargs={'category_id':self.category.id}), {
            'title': 'My Topic',
            'text': 'Lqlqlq',
            'author': self.student_user,
            'category': self.category,
        })
        after_add = Topic.objects.count()

        self.assertEqual(before_add, after_add)
        self.assertRedirects(response, 'login/?next=/add-topic/1/')