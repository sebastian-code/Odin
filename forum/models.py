from django.conf import settings
from django.core.mail import send_mass_mail
from django.db import models
from django.template.loader import render_to_string

from students.models import User


class Category(models.Model):
    title = models.CharField(blank=False, max_length=128)
    text = models.CharField(blank=False, max_length=512)
    ordering = models.PositiveSmallIntegerField(default=0, blank=False, null=False)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'categories'
        ordering = ('ordering',)


class Topic(models.Model):
    title = models.CharField(blank=False, max_length=128)
    text = models.TextField(blank=False)
    author = models.ForeignKey(User)
    category = models.ForeignKey(Category)
    date = models.DateField(auto_now=True)

    def __str__(self):
        return self.title

    def send_mails(self, comment):
        users = User.objects.filter(subscribed_topics=self)
        emails = []
        for user in users:
            if comment.author != user:
                context = {
                    'author': comment.author.get_full_name(),
                    'name': user.get_full_name(),
                    'domain': settings.DOMAIN,
                    'topic': self.title,
                    'topic_id': self.id,
                    'comment': comment.id
                }

                message = render_to_string('send_topic_subscribe_email.html', context)
                emails.append((
                    'Hack Bulgaria new comment in "{0}"'.format(self.title),
                    message,
                    settings.DEFAULT_FROM_EMAIL,
                    (user.email,)
                ))
        send_mass_mail(emails)

    def subscribe(self, user):
        if self not in user.subscribed_topics.all():
            user.subscribed_topics.add(self)
            user.save()

    def unsubscribe(self, user):
        if self in user.subscribed_topics.all():
            user.subscribed_topics.remove(self)
            user.save()


class Comment(models.Model):
    text = models.TextField(blank=False)
    author = models.ForeignKey(User)
    topic = models.ForeignKey(Topic)

    def __str__(self):
        return self.text
