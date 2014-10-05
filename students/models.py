import string
import random

from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.contrib.auth.signals import user_logged_in

from django_resized import ResizedImageField

from courses.models import Course, Partner, Task
from validators import validate_mac, validate_github, validate_linkedin


class UserManager(BaseUserManager):

    def __create_user(self, email, password, is_staff, is_superuser,
                      first_name, last_name, works_at):
        if not email:
            raise ValueError('Users must have an email address')

        email = self.normalize_email(email)
        user = self.model(username=email, email=email,
                          is_staff=is_staff, is_superuser=is_superuser,
                          first_name=first_name, last_name=last_name,
                          works_at=works_at)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, first_name='', last_name='', works_at=None):
        return self.__create_user(email, password, False, False,
                                  first_name, last_name, works_at)

    def create_superuser(self, email, password, first_name='', last_name='', works_at=None):
        return self.__create_user(email, password, True, True,
                                  first_name, last_name, works_at)


class User(AbstractUser):
    STUDENT = 1
    HR = 2
    TEACHER = 3

    STATUSES = (
        (STUDENT, 'Student'),
        (HR, 'HR'),
        (TEACHER, 'Teacher'),

    )

    status = models.SmallIntegerField(choices=STATUSES, default=STUDENT)

    avatar = ResizedImageField(
        upload_to='avatar',
        max_width=200,
        blank=True,
    )

    courses = models.ManyToManyField(Course, through='CourseAssignment')
    description = models.TextField(blank=True)
    github_account = models.URLField(validators=[validate_github], null=True, blank=True)
    hr_of = models.ForeignKey(Partner, blank=True, null=True)
    linkedin_account = models.URLField(validators=[validate_linkedin], null=True, blank=True)
    mac = models.CharField(validators=[validate_mac], max_length=17, null=True, blank=True)
    subscribed_topics = models.ManyToManyField('forum.Topic', blank=True)
    works_at = models.CharField(null=True, blank=True, max_length='40')

    AbstractUser._meta.get_field('email')._unique = True

    AbstractUser.REQUIRED_FIELDS.remove('email')
    AbstractUser._meta.get_field('username').max_length = 75
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __unicode__(self):
        return unicode(self.get_full_name())

    def is_existing(self, email):
        return User.objects.filter(email=email).count() > 0

    @staticmethod
    def generate_password(size=9, chars=string.ascii_uppercase + string.digits):
        return ''.join(random.choice(chars) for x in range(size))

    def get_avatar_url(self):
        if not self.avatar:
            return settings.STATIC_URL + settings.NO_AVATAR_IMG
        return self.avatar.url

    def get_courses(self):
        return '; '.join([courseassignment.course.name + ' - ' + str(courseassignment.group_time)
                          for courseassignment
                          in self.courseassignment_set.all()])

    def get_courses_list(self):
        courses = []
        for course in self.courseassignment_set.all():
            courses.append(course)
        return courses

    def log_hr_login(sender, user, request, **kwargs):
        if user.status == User.HR:
            log = HrLoginLog(user=user)
            log.save()

    user_logged_in.connect(log_hr_login)


class HrLoginLog(models.Model):
    user = models.ForeignKey(User)
    date = models.DateField(auto_now=True)


class CourseAssignment(models.Model):
    EARLY = 1
    LATE = 2

    GROUP_TIME_CHOICES = (
        (EARLY, 'Early'),
        (LATE, 'Late'),
    )

    course = models.ForeignKey(Course)
    cv = models.FileField(blank=True, null=True, upload_to='cvs')
    favourite_partners = models.ManyToManyField(Partner)
    group_time = models.SmallIntegerField(choices=GROUP_TIME_CHOICES)
    points = models.PositiveIntegerField(default=0)
    user = models.ForeignKey(User)

    def __unicode__(self):
        return u'<{}> {} - {}'.format(self.user.get_full_name(), self.course, self.group_time)

    def get_favourite_partners(self):
        return '; '.join([partner.name for partner in self.favourite_partners.all()])

    def has_valid_github_account(self):
        github_account = self.user.github_account
        return github_account is not None and '://github.com/' in github_account

    class Meta:
        unique_together = (('user', 'course'),)


class StudentStartedWorkingAt(models.Model):
    assignment = models.ForeignKey(CourseAssignment)
    partner = models.ForeignKey(Partner, blank=True, null=True)
    partner_name = models.CharField(max_length=128, blank=True, null=True)

    def __unicode__(self):
        return u'{} - {}'.format(self.assignment, self.partner)


class UserNote(models.Model):
    text = models.TextField(blank=True)
    assignment = models.ForeignKey(CourseAssignment)
    author = models.ForeignKey(User, null=True, blank=True)
    post_time = models.DateTimeField(auto_now=True)


class CheckIn(models.Model):
    mac = models.CharField(max_length=17)
    student = models.ForeignKey(User, null=True, blank=True)
    date = models.DateField(auto_now=True)

    class Meta:
        unique_together = ('student', 'date')


class Solution(models.Model):
    task = models.ForeignKey(Task)
    user = models.ForeignKey(User)
    repo = models.URLField()

    def __parse_github_url(self, github_url):
        github_url_split = github_url.split('/')[3:]
        # Ex: https://github.com/syndbg/HackBulgaria/tree/master/Core-Java-1
        # Becomes  [u'https:', u'', u'github.com', u'syndbg', u'HackBulgaria', u'tree', u'master', u'Core-Java-1']
        # Only 4th and 5th elements are relevant
        return {'user_name': github_url_split[0], 'repo_name': github_url_split[1]} if len(github_url_split) >= 2 else {'user_name': github_url_split[0]}

    def get_user_github_username(self):
        return self.__parse_github_url(self.user.github_account)['user_name']

    def get_github_user_and_repo_names(self):
        return self.__parse_github_url(self.repo)

    class Meta:
        unique_together = (('user', 'task'),)
