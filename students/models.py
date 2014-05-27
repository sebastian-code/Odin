from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser, BaseUserManager, PermissionsMixin
from django_resized import ResizedImageField
from courses.models import Course


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
    avatar = ResizedImageField(
        upload_to='link_images',
        max_width=200,
    )
    github_account = models.URLField(null=True, blank=True)
    linkedin_account = models.URLField(null=True, blank=True)
    description = models.TextField(blank=True)
    courses = models.ManyToManyField(Course, through='CourseAssignment')

    AbstractUser._meta.get_field('email')._unique = True
    AbstractUser.REQUIRED_FIELDS.remove('email')

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    def __unicode__(self):
        return unicode(self.username)

    def getAvatarUrl(self):
        if not self.avatar:
            return settings.STATIC_URL + settings.NO_AVATAR_IMG 
        return self.avatar.url

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

    class Meta:
        unique_together = ('user', 'course')

    def __unicode__(self):
        return unicode('{} - {}'.format(self.user, self.course))


class UserNote(models.Model):
    text = models.TextField(blank=True)
    assignment = models.ForeignKey(CourseAssignment)
    author = models.ForeignKey(User, null=True, blank=True)
    post_time = models.DateTimeField(auto_now=True)


