from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser, BaseUserManager, PermissionsMixin
from django_resized import ResizedImageField
from courses.models import Course, Partner
from django.core.exceptions import ValidationError
from django.contrib.auth.signals import user_logged_in

import re

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
        user.username = email
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

    github_account = models.URLField(null=True, blank=True)
    linkedin_account = models.URLField(null=True, blank=True)
    description = models.TextField(blank=True)
    courses = models.ManyToManyField(Course, through='CourseAssignment')
    mac = models.CharField(max_length=17, null=True, blank=True)
    works_at = models.CharField(null=True, blank=True, max_length="40")
    subscribed_topics = models.ManyToManyField('forum.Topic', blank=True)

    AbstractUser._meta.get_field('email')._unique = True
    AbstractUser.REQUIRED_FIELDS.remove('email')
    AbstractUser._meta.get_field('username').max_length=75
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    def __unicode__(self):
        return unicode(self.get_full_name())


    def getAvatarUrl(self):
        if not self.avatar:
            return settings.STATIC_URL + settings.NO_AVATAR_IMG 
        return self.avatar.url


    def get_courses(self):
        return "; ".join([courseassignment.course.name + ' - ' + str(courseassignment.group_time) 
            for courseassignment 
                in self.courseassignment_set.all()])

    def get_courses_list(self):
        courses = []
        for course in self.courseassignment_set.all():
            courses.append(course)

        return courses

    def clean(self, *args, **kwargs):
        if self.mac:
            mac_pattern = re.compile(r'^([0-9A-F]{2}[:]){5}([0-9A-F]{2})$', re.IGNORECASE)
            if not re.match(mac_pattern, self.mac):
                raise ValidationError(u'%s is not a valid mac address' % self.mac)
            self.mac = self.mac.lower()

        super(AbstractUser, self).clean(*args, **kwargs)

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

    user = models.ForeignKey(User)
    course = models.ForeignKey(Course)
    points = models.PositiveIntegerField(default='0')
    group_time = models.SmallIntegerField(choices=GROUP_TIME_CHOICES)
    favourite_partners = models.ManyToManyField(Partner)
    cv = models.FileField(blank=True, null=True, upload_to='cvs')

    class Meta:
        unique_together = ('user', 'course')

    def __str__(self):
        return unicode('{} - {}'.format(self.course, self.group_time))

    def get_favourite_partners(self):
        return "; ".join([partner.name 
            for partner 
                in self.favourite_partners.all()])


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