from django.core.mail import send_mass_mail
from django.conf import settings
from students.models import User
from .models import Comment

def send_topic_subscribe_email(topic, comment):
    users = User.objects.filter(subscribed_topics=topic)
    emails = []
    for user in users:
        if comment.author != user:
            message = open(settings.BASE_DIR + '/forum/templates/email/send_topic_subscribe_email.txt').read()
            
            message = message.format(
                user.get_full_name().encode('utf8'), 
                settings.DOMAIN, 
                topic.id, 
                comment.id
            )
            
            emails.append((
                'Hack Bulgaria new comment in "{}"'.format(topic.title.encode('utf8')), 
                message, 
                settings.DEFAULT_FROM_EMAIL, 
                (user.email,)
            ))

    send_mass_mail(emails)


def subscribe_to_topic(user, topic):
    users_comments_for_topic = Comment.objects.filter(author=user, topic=topic).count()

    #Checking if this is the first comment
    if users_comments_for_topic <= 1:
        user.subscribed_topics.add(topic)
        user.save()