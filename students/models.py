from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.contrib.auth.signals import user_logged_in

from courses.models import Course, Partner, Task
from validators import validate_mac, validate_github, validate_linkedin

from django_resized import ResizedImageField


class UserManager(BaseUserManager):

    def create_user(self, email, password=None):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=UserManager.normalize_email(email),
        )
        user.username = email
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        user = self.create_user(email, password=password)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


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
    github_account = models.URLField(validators=[validate_github], blank=True)
    hr_of = models.ForeignKey(Partner, blank=True, null=True)
    linkedin_account = models.URLField(validators=[validate_linkedin], blank=True)
    mac = models.CharField(validators=[validate_mac], max_length=17, blank=True)
    subscribed_topics = models.ManyToManyField('forum.Topic', blank=True)
    works_at = models.CharField(blank=True, max_length='40')

    AbstractUser._meta.get_field('email')._unique = True

    AbstractUser.REQUIRED_FIELDS.remove('email')
    AbstractUser._meta.get_field('username').max_length = 75
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __unicode__(self):
        return unicode(self.get_full_name())

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

    after_course_works_at = models.ForeignKey(Partner, related_name='after_course_works', blank=True, null=True)
    user = models.ForeignKey(User)
    course = models.ForeignKey(Course)
    points = models.PositiveIntegerField(default=0)
    group_time = models.SmallIntegerField(choices=GROUP_TIME_CHOICES)
    cv = models.FileField(blank=True, upload_to='cvs', default='')
    favourite_partners = models.ManyToManyField(Partner)

    class Meta:
        unique_together = (('user', 'course'),)

    def __unicode__(self):
        return u'<{}> {} - {}'.format(self.user.get_full_name(), self.course, self.group_time)

    def get_favourite_partners(self):
        return '; '.join([partner.name for partner in self.favourite_partners.all()])

    def has_valid_github_account(self):
        github_account = self.user.github_account
        return github_account is not None and '://github.com/' in github_account


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
