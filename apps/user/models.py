"""
(C) 2016 - Laszlo Marai <atleta@atleta.hu>
"""
import logging
import re

from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import (AbstractBaseUser, PermissionsMixin)
from django.core import validators
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from apps.user.utils import UploadDir

logger = logging.getLogger(__name__)


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, **kwargs):
        """
        Creates and saves a User with the given email and password.
        """
        if not kwargs.get(self.model.USERNAME_FIELD, None):
            raise ValueError('The USERNAME_FIELD (%s) must be provided' % self.model.USERNAME_FIELD)

        # TODO: clean this up and make generic. Why is username normalized by the model and email by the manager?
        for k, v in kwargs.items():
            method_name = 'normalize_%s' % k
            normalizer = getattr(self, method_name, getattr(self.model, method_name, None))
            if normalizer:
                kwargs[k] = normalizer(v)

        password = kwargs.pop('password')
        user = self.model(**kwargs)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, **kwargs):
        kwargs.setdefault('is_superuser', False)
        return self._create_user(**kwargs)

    def create_superuser(self, **kwargs):
        kwargs.setdefault('is_superuser', True)
        kwargs.setdefault('is_staff', True)

        if kwargs.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if kwargs.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(**kwargs)


class User(AbstractBaseUser, PermissionsMixin):
    GENDER = (
        ('male', 'Male'),
        ('female', 'Female'),
    )

    email = models.EmailField(_('email address'), unique=True, db_index=True, validators=[validators.EmailValidator()])
    username = models.CharField(_('username'), max_length=30, unique=True,
                                help_text=_(
                                    'Required. 30 characters or fewer. Letters, numbers and '
                                    '@/./+/-/_ characters'),
                                validators=[
                                    validators.RegexValidator(re.compile('^[\w.+-]+$'),
                                                              _('Enter a valid username.'),
                                                              'invalid')
                                ],
                                error_messages={
                                    'unique': _("User with this username already exists."),
                                }, )

    full_name = models.CharField(_('full name'), max_length=60)
    is_staff = models.BooleanField(_('staff status'), default=False,
                                   help_text=_(
                                       'Designates whether the user can log into this admin '
                                       'site.'))
    is_active = models.BooleanField(_('active'), default=True,
                                    help_text=_(
                                        'Designates whether this user should be treated as '
                                        'active. Unselect this instead of deleting accounts.'))
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    followers = models.ManyToManyField('User', related_name='following', through='Follow')

    photo = models.FileField(blank=True, upload_to=UploadDir('photo'))
    age = models.PositiveSmallIntegerField(blank=True, null=True)
    gender = models.CharField(max_length=6, choices=GENDER)
    address = models.CharField(_('address'), max_length=255, null=True)
    phone = models.CharField(_('phone'), max_length=255, null=True)
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def get_full_name(self):
        """
        Returns the full name.
        """
        return '%s' % self.full_name

    def follow(self, other_user):
        return Follow.objects.create(to_user=self, from_user=other_user)

    def unfollow(self, other_user):
        Follow.objects.filter(to_user=self, from_user=other_user).delete()

    def add_follower(self, other_user):
        return other_user.follow(self)

    def remove_follower(self, other_user):
        other_user.unfollow(self)


class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    primary_picture = models.ImageField(upload_to=UploadDir('product_images'))


class ProductPicture(models.Model):
    product = models.ForeignKey(Product, related_name='pictures', on_delete=models.CASCADE)
    picture = models.ImageField(upload_to=UploadDir('product_images'))


class Hashtag(models.Model):
    name = models.CharField(max_length=100)


class Follow(models.Model):
    from_user = models.ForeignKey(User, related_name='from_user', on_delete=models.CASCADE)
    to_user = models.ForeignKey(User, related_name='to_user', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    @property
    def feed_order(self):
        return self.created


class Trending(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    profiles = models.ManyToManyField(User, through='TrendingProfile')
    hashtags = models.ManyToManyField(Hashtag, through='TrendingHashtag')


class TrendingProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    trending = models.ForeignKey(Trending, on_delete=models.CASCADE)
    score = models.DecimalField(max_digits=9, decimal_places=2, default=0, unique=False)

    class Meta:
        ordering = ('-score',)


class TrendingHashtag(models.Model):
    hashtag = models.ForeignKey(Hashtag, on_delete=models.CASCADE)
    trending = models.ForeignKey(Trending, on_delete=models.CASCADE)
    score = models.DecimalField(max_digits=9, decimal_places=2, default=0, unique=False)

    class Meta:
        ordering = ('-score',)


class TaskRunManager(models.Manager):
    def last_run_at(self, task_label):
        return TaskRun.objects.filter(task_label=task_label).order_by('-started_at'). \
            values_list('started_at', flat=True).first()


class TaskRun(models.Model):
    objects = TaskRunManager()

    # Keep track of celery tasks
    task_label = models.CharField(_('task label'), max_length=30)
    started_at = models.DateTimeField(auto_now_add=True)
    terminated_at = models.DateTimeField(default=None, null=True, blank=True)

    class Meta:
        ordering = ('-started_at',)
