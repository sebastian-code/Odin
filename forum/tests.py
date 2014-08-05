# -*- coding: utf-8 -*-
from django.test import TestCase, client
from django.core import mail
from django.core.urlresolvers import reverse

from students.models import User
from .models import Category, Topic, Comment


class CoursesTest(TestCase):
    def setUp(self):
        self.student_user = User.objects.create_user('ivo_student@gmail.com', '123')
        self.student_user.status = User.STUDENT
        # self.student_user.first_name = "Иван"
        self.student_user.save()

        self.hr_user = User.objects.create_user('ivo_hr@gmail.com', '123')
        self.hr_user.status = User.HR
        self.hr_user.save()

        self.category = Category.objects.create(
            title='Test Category',
        )

        self.topic = Topic.objects.create(
            title='Test Topic',
            author=self.student_user,
            category=self.category,
        )

        self.comment = Comment.objects.create(
            text='Test Comment',
            author=self.student_user,
            topic=self.topic,
        )

    def test_show_categories_status(self):
        self.client = client.Client()
        response = self.client.get(reverse('forum:forum'))
        self.assertEqual(200, response.status_code)

    def test_show_category_status(self):
        self.client = client.Client()
        response = self.client.get(
            reverse('forum:show-category', kwargs={'category_id': self.category.id}))
        self.assertEqual(200, response.status_code)

    def test_show_nonexistent_category_status(self):
        self.client = client.Client()
        response = self.client.get(reverse('forum:show-category', kwargs={'category_id': '234'}))
        self.assertEqual(404, response.status_code)

    def test_show_topic_status(self):
        self.client = client.Client()
        response = self.client.get(reverse('forum:show-topic', kwargs={'topic_id': self.topic.id}))
        self.assertEqual(200, response.status_code)

    def test_show_nonexistent_topic_status(self):
        self.client = client.Client()
        response = self.client.get(reverse('forum:show-topic', kwargs={'topic_id': '234'}))
        self.assertEqual(404, response.status_code)

    def test_add_topic_status(self):
        self.client = client.Client()
        self.client.login(username='ivo_student@gmail.com', password='123')
        before_add = Topic.objects.count()
        response = self.client.post(reverse('forum:add-topic',  kwargs={'category_id': self.category.id}), {
            'title': 'My Topic',
            'text': 'Lqlqlq',
            'category': self.category,
        })

        after_add = Topic.objects.count()
        self.assertEqual(before_add + 1, after_add)

    def test_add_topic_not_logged_redirect(self):
        self.client = client.Client()

        before_add = Topic.objects.count()
        response = self.client.post(reverse('forum:add-topic',  kwargs={'category_id': self.category.id}), {
            'title': 'My Topic',
            'text': 'Lqlqlq',
            'category': self.category,
        })
        after_add = Topic.objects.count()

        self.assertEqual(before_add, after_add)
        self.assertRedirects(response, 'login/?next=/add-topic/1/')

    def test_edit_topic(self):
        self.client = client.Client()
        self.client.login(username='ivo_student@gmail.com', password='123')
        response = self.client.post(reverse('forum:edit-topic',  kwargs={'topic_id': self.topic.id}), {
            'title': 'My Topic 2',
            'text': 'Lqlqlq lqlql',
        })

        self.assertRedirects(response, 'topic/1/')

    def test_edit_not_logged(self):
        self.client = client.Client()
        response = self.client.post(reverse('forum:edit-topic',  kwargs={'topic_id': self.topic.id}), {
            'title': 'My Topic 2',
            'text': 'Lqlqlq lqlql',
        })

        self.assertRedirects(response, 'login/?next=/edit-topic/1/')

    def test_edit_not_owned(self):
        self.client = client.Client()
        self.client.login(username='ivo_hr@gmail.com', password='123')
        response = self.client.post(reverse('forum:edit-topic',  kwargs={'topic_id': self.topic.id}), {
            'title': 'My Topic 2',
            'text': 'Lqlqlq lqlql',
        })

        self.assertEqual(403, response.status_code)

    def test_add_comment(self):
        self.client = client.Client()
        self.client.login(username='ivo_student@gmail.com', password='123')
        before_add = Comment.objects.count()
        response = self.client.post(reverse('forum:show-topic', kwargs={'topic_id': self.topic.id}), {
            'text': 'Lqlqlq',
            'topic': self.topic,
        })

        after_add = Comment.objects.count()
        self.assertEqual(before_add + 1, after_add)

    def test_edit_comment(self):
        self.client = client.Client()
        self.client.login(username='ivo_student@gmail.com', password='123')
        new_text = 'New text of the comment'
        response = self.client.post(reverse('forum:edit-comment', kwargs={'comment_id': self.comment.id}), {
            'text': new_text,
        })

        self.assertRedirects(response, 'topic/1/')
        edited_comment = Comment.objects.filter(text=new_text).count()
        self.assertEqual(edited_comment, 1)

    def test_edit_comment_not_owned(self):
        self.client = client.Client()
        self.client.login(username='ivo_hr@gmail.com', password='123')
        new_text = 'New text of the comment'
        response = self.client.post(reverse('forum:edit-comment', kwargs={'comment_id': self.comment.id}), {
            'text': new_text,
        })

        self.assertEqual(403, response.status_code)

    def test_add_comment_not_logged(self):
        self.client = client.Client()
        before_add = Comment.objects.count()
        response = self.client.post(reverse('forum:show-topic', kwargs={'topic_id': self.topic.id}), {
            'text': 'Lqlqlq',
            'topic': self.topic,
        })

        after_add = Comment.objects.count()
        self.assertEqual(before_add, after_add)

# Testing subscribitons
    def test_unsubscribing(self):
        self.client = client.Client()

        self.client.login(
            username=self.student_user.email,
            password='123',
        )

        self.student_user.subscribed_topics.add(self.topic)
        self.student_user.save()

        response = self.client.get(
            reverse('forum:unsubscribe', kwargs={'topic_id': self.topic.id})
        )

        self.assertEqual(200, response.status_code)
        self.assertTrue(self.topic not in self.student_user.subscribed_topics.all())

    def test_subscribing(self):
        self.client = client.Client()

        self.client.login(
            username=self.student_user.email,
            password='123',
        )

        response = self.client.get(
            reverse('forum:subscribe', kwargs={'topic_id': self.topic.id})
        )

        self.assertEqual(200, response.status_code)
        self.assertTrue(self.topic in self.student_user.subscribed_topics.all())

    def test_subscribing_unlogged(self):
        response = self.client.get(
            reverse('forum:unsubscribe', kwargs={'topic_id': self.topic.id})
        )

        self.assertEqual(302, response.status_code)

    def test_subscribing_afther_new_topic(self):
        self.client = client.Client()
        self.client.login(
            username=self.student_user.email,
            password='123'
        )

        response = self.client.post(
            reverse('forum:add-topic',  kwargs={'category_id': self.category.id}),
            {
                'title': 'test subscriging afther new topic',
                'text': 'Lqlqlq',
                'category': self.category,
            }
        )

        new_topic = Topic.objects.filter(title="test subscriging afther new topic").first()
        self.assertTrue(new_topic in self.student_user.subscribed_topics.all())

    def test_subscribing_afther_new_topic(self):
        self.client = client.Client()
        self.client.login(
            username=self.student_user.email,
            password='123'
        )

        response = self.client.post(
            reverse('forum:add-topic',  kwargs={'category_id': self.category.id}),
            {
                'title': 'test subscriging afther new topic',
                'text': 'Lqlqlq',
                'category': self.category,
            }
        )

        new_topic = Topic.objects.filter(title="test subscriging afther new topic").first()
        self.assertTrue(new_topic in self.student_user.subscribed_topics.all())

    def test_subscribing_afther_new_comment(self):
        self.client = client.Client()
        self.client.login(
            username=self.student_user.email,
            password='123'
        )

        empty_topic = Topic.objects.create(
            title='Test for new comment',
            author=self.student_user,
            category=self.category,
        )

        response = self.client.post(reverse('forum:show-topic', kwargs={'topic_id': empty_topic.id}), {
            'text': 'Lqlqlq lqlqlql lqlqlql',
            'topic': empty_topic,
        })

        self.assertTrue(empty_topic in self.student_user.subscribed_topics.all())

    def test_subscribing_afther_unsubscribing(self):
        self.client = client.Client()
        self.client.login(
            username=self.student_user.email,
            password='123',
        )

        empty_topic = Topic.objects.create(
            title='Test for new comment',
            author=self.student_user,
            category=self.category,
        )

        response = self.client.post(reverse('forum:show-topic', kwargs={'topic_id': empty_topic.id}), {
            'text': 'Lqlqlq lqlqlql lqlqlql',
            'topic': empty_topic,
        })

        response = self.client.get(
            reverse('forum:unsubscribe', kwargs={'topic_id': empty_topic.id})
        )

        response = self.client.post(reverse('forum:show-topic', kwargs={'topic_id': empty_topic.id}), {
            'text': 'Lqlqlq lqlqlql lqlqlql2',
            'topic': empty_topic,
        })

        self.assertTrue(empty_topic not in self.student_user.subscribed_topics.all())

    def test_sending_emails(self):
        self.client = client.Client()
        self.client.login(
            username=self.student_user.email,
            password='123',
        )

        response = self.client.post(
            reverse('forum:add-topic',  kwargs={'category_id': self.category.id}),
            {
                'title': 'test sending emails',
                'text': 'Lqlqlq',
                'category': self.category,
            }
        )

        new_topic = Topic.objects.filter(title="test sending emails").first()

        self.client.logout()
        self.client.login(
            username=self.hr_user.email,
            password='123',
        )

        response = self.client.post(reverse('forum:show-topic', kwargs={'topic_id': new_topic.id}), {
            'text': 'Lqlqlq lqlqlql lqlqlql23',
            'topic': new_topic,
        })

        self.assertEqual(1, len(mail.outbox))

    def test_new_comment_email_title(self):
        self.client = client.Client()
        self.client.login(
            username=self.student_user.email,
            password='123',
        )

        response = self.client.post(
            reverse('forum:add-topic',  kwargs={'category_id': self.category.id}),
            {
                'title': 'Нова тема тряляля',
                'text': 'Lqlqlq',
                'category': self.category,
            }
        )

        new_topic = Topic.objects.filter(title="Нова тема тряляля").first()

        self.client.logout()
        self.client.login(
            username=self.hr_user.email,
            password='123',
        )

        response = self.client.post(reverse('forum:show-topic', kwargs={'topic_id': new_topic.id}), {
            'text': 'Lqlqlq lqlqlql lqlqlql23',
            'topic': new_topic,
        })

        self.assertTrue(mail.outbox[0].subject.find(new_topic.title.encode("utf-8")))
