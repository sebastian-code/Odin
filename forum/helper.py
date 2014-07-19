from django.core.mail import send_mass_mail
from django.conf import settings
from students.models import User


def send_topic_subscribe_email(topic, comment):
    users = User.objects.filter(subscribed_topics=topic)
    emails = []
    for user in users:
        message = open(settings.BASE_DIR + '/forum/templates/email/send_topic_subscribe_email.txt').read()
        message = message.format(user.get_full_name(), settings.DOMAIN, topic.id, comment.id)
        emails.append(('Hack Bulgaria forum new comment', message, settings.DEFAULT_FROM_EMAIL, (user.email,)))

    print send_mass_mail(emails)
