# -*- coding: utf-8 -*-
from django.test import TestCase
from django.core import mail
from django.core.urlresolvers import reverse

from students.models import User
from .models import Category, Topic, Comment


class ForumViewsTest(TestCase):

    def setUp(self):
        self.student_user = User.objects.create_user('ivo_student@gmail.com', '123')
        self.student_user.status = User.STUDENT
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

    def test_show_categories(self):
        response = self.client.get(reverse('forum:forum'))
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed('categories.html', response)

    def test_show_category(self):
        response = self.client.get(
            reverse('forum:show_category', kwargs={'category_id': self.category.id}))
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed('show_category.html', response)

    def test_show_nonexistent_category(self):
        response = self.client.get(reverse('forum:show_category', kwargs={'category_id': '234'}))
        self.assertEqual(404, response.status_code)
        self.assertTemplateNotUsed('show_category.html', response)

    def test_show_topic(self):
        response = self.client.get(reverse('forum:show_topic', kwargs={'topic_id': self.topic.id}))
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed('show_topic.html', response)

    def test_show_nonexistent_topic(self):
        response = self.client.get(reverse('forum:show_topic', kwargs={'topic_id': '234'}))
        self.assertEqual(404, response.status_code)
        self.assertTemplateNotUsed('show_topic.html', response)

    def test_add_topic(self):
        self.client.login(username='ivo_student@gmail.com', password='123')
        before_add = Topic.objects.count()
        response = self.client.post(reverse('forum:add_topic',  kwargs={'category_id': self.category.id}), {
            'title': 'My Topic',
            'text': 'Lqlqlq',
            'category': self.category,
        })

        after_add = Topic.objects.count()
        self.assertEqual(before_add + 1, after_add)
        self.assertEqual(302, response.status_code)
        self.assertRedirects(response, 'forum/category/{}/'.format(self.category.id))
        self.assertTemplateUsed('add_topic.html', response)

    def test_add_topic_not_logged_redirect(self):
        before_add = Topic.objects.count()
        response = self.client.post(reverse('forum:add_topic',  kwargs={'category_id': self.category.id}), {
            'title': 'My Topic',
            'text': 'Lqlqlq',
            'category': self.category,
        })
        after_add = Topic.objects.count()

        self.assertEqual(before_add, after_add)
        self.assertEqual(302, response.status_code)
        self.assertRedirects(response, 'login/?next=/forum/add-topic/{}/'.format(self.category.id))
        self.assertTemplateNotUsed('add_topic.html', response)

    def test_edit_topic(self):
        self.client.login(username='ivo_student@gmail.com', password='123')
        response = self.client.post(reverse('forum:edit_topic',  kwargs={'topic_id': self.topic.id}), {
            'title': 'My Topic 2',
            'text': 'Lqlqlq lqlql',
        })

        edited_topic = Topic.objects.filter(title='My Topic 2')
        self.assertEqual(1, edited_topic.count())
        self.assertEqual(302, response.status_code)
        self.assertTemplateUsed('edit_topic.html', response)

    def test_edit_topic_not_logged(self):
        response = self.client.post(reverse('forum:edit_topic',  kwargs={'topic_id': self.topic.id}), {
            'title': 'My Topic 2',
            'text': 'Lqlqlq lqlql',
        })

        self.assertEqual(302, response.status_code)
        self.assertRedirects(response, 'login/?next=/forum/edit-topic/{}/'.format(self.topic.id))
        self.assertTemplateNotUsed('edit_topic.html', response)

    def test_edit_topic_not_owned(self):
        self.client.login(username='ivo_hr@gmail.com', password='123')
        response = self.client.post(reverse('forum:edit_topic',  kwargs={'topic_id': self.topic.id}), {
            'title': 'My Topic 2',
            'text': 'Lqlqlq lqlql',
        })

        self.assertEqual(403, response.status_code)
        self.assertTemplateNotUsed('edit_topic.html', response)

    def test_add_comment(self):
        self.client.login(username='ivo_student@gmail.com', password='123')
        before_add = Comment.objects.count()
        response = self.client.post(reverse('forum:show_topic', kwargs={'topic_id': self.topic.id}), {
            'text': 'Lqlqlq',
            'topic': self.topic,
        })

        after_add = Comment.objects.count()
        self.assertEqual(before_add + 1, after_add)
        self.assertEqual(302, response.status_code)
        self.assertTemplateUsed('show_topic.html', response)

    def test_add_comment_not_logged(self):
        before_add = Comment.objects.count()
        response = self.client.post(reverse('forum:show_topic', kwargs={'topic_id': self.topic.id}), {
            'text': 'Lqlqlq',
            'topic': self.topic,
        })

        after_add = Comment.objects.count()
        self.assertEqual(before_add, after_add)
        self.assertEqual(200, response.status_code)
        self.assertTemplateNotUsed('show_topic.html', response)

    def test_edit_comment(self):
        self.client.login(username='ivo_student@gmail.com', password='123')
        new_text = 'New text of the comment'
        response = self.client.post(reverse('forum:edit_comment', kwargs={'comment_id': self.comment.id}), {
            'text': new_text,
        })

        edited_comment = Comment.objects.get(text=new_text)
        self.assertEqual(302, response.status_code)
        self.assertRedirects(response, 'forum/topic/{}/'.format(self.comment.id))
        self.assertTemplateUsed('edit_comment.html', response)

    def test_edit_comment_not_owned(self):
        self.client.login(username='ivo_hr@gmail.com', password='123')
        new_text = 'New text of the comment'
        response = self.client.post(reverse('forum:edit_comment', kwargs={'comment_id': self.comment.id}), {
            'text': new_text,
        })

        self.assertEqual(403, response.status_code)
        self.assertTemplateNotUsed('edit_comment.html', response)

    # Testing subscriptions
    def test_unsubscribing(self):
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

    def test_subscribing_after_new_topic(self):
        self.client.login(
            username=self.student_user.email,
            password='123'
        )

        response = self.client.post(
            reverse('forum:add_topic',  kwargs={'category_id': self.category.id}),
            {
                'title': 'test subscribing after new topic',
                'text': 'Lqlqlq',
                'category': self.category,
            }
        )

        new_topic = Topic.objects.filter(title="test subscribing after new topic").first()
        self.assertTrue(new_topic in self.student_user.subscribed_topics.all())
        self.assertEqual(302, response.status_code)
        self.assertTemplateUsed('add_topic.html', response)

    def test_subscribing_after_new_comment(self):
        self.client.login(
            username=self.student_user.email,
            password='123'
        )

        empty_topic = Topic.objects.create(
            title='Test for new comment',
            author=self.student_user,
            category=self.category,
        )

        response = self.client.post(reverse('forum:show_topic', kwargs={'topic_id': empty_topic.id}), {
            'text': 'Lqlqlq lqlqlql lqlqlql',
            'topic': empty_topic,
        })

        self.assertEqual(302, response.status_code)
        self.assertTrue(empty_topic in self.student_user.subscribed_topics.all())
        self.assertTemplateUsed('show_topic.html', response)

    def test_subscribing_after_unsubscribing(self):
        self.client.login(
            username=self.student_user.email,
            password='123',
        )

        empty_topic = Topic.objects.create(
            title='Test for new comment',
            author=self.student_user,
            category=self.category,
        )

        response = self.client.post(reverse('forum:show_topic', kwargs={'topic_id': empty_topic.id}), {
            'text': 'Lqlqlq lqlqlql lqlqlql',
            'topic': empty_topic,
        })

        response = self.client.get(
            reverse('forum:unsubscribe', kwargs={'topic_id': empty_topic.id})
        )

        response = self.client.post(reverse('forum:show_topic', kwargs={'topic_id': empty_topic.id}), {
            'text': 'Lqlqlq lqlqlql lqlqlql2',
            'topic': empty_topic,
        })

        self.assertEqual(302, response.status_code)
        self.assertTrue(empty_topic not in self.student_user.subscribed_topics.all())
        self.assertTemplateUsed('show_topic.html', response)

    def test_sending_emails(self):
        self.client.login(
            username=self.student_user.email,
            password='123',
        )

        response = self.client.post(
            reverse('forum:add_topic',  kwargs={'category_id': self.category.id}),
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

        response = self.client.post(reverse('forum:show_topic', kwargs={'topic_id': new_topic.id}), {
            'text': 'Lqlqlq lqlqlql lqlqlql23',
            'topic': new_topic,
        })

        self.assertEqual(1, len(mail.outbox))

    def test_new_comment_email_title(self):
        self.client.login(
            username=self.student_user.email,
            password='123',
        )

        response = self.client.post(
            reverse('forum:add_topic',  kwargs={'category_id': self.category.id}),
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

        response = self.client.post(reverse('forum:show_topic', kwargs={'topic_id': new_topic.id}), {
            'text': 'Lqlqlq lqlqlql lqlqlql23',
            'topic': new_topic,
        })

        self.assertTrue(mail.outbox[0].subject.find(new_topic.title.encode("utf-8")))
