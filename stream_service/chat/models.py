import datetime
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class EmailUserManager(BaseUserManager):

    """Custom manager for EmailUser."""

    def _create_user(self, email, password,
                     is_staff, is_superuser, **extra_fields):
        """Create and save an EmailUser with the given email and password.

        :param str email: user email
        :param str password: user password
        :param bool is_staff: whether user staff or not
        :param bool is_superuser: whether user admin or not
        :return custom_user.models.EmailUser user: user
        :raise ValueError: email is not set

        """
        now = datetime.datetime.now()
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        is_active = extra_fields.pop("is_active", True)
        user = self.model(email=email, is_staff=is_staff, is_active=is_active,
                          is_superuser=is_superuser, last_login=now,
                          date_joined=now, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save an EmailUser with the given email and password.

        :param str email: user email
        :param str password: user password
        :return custom_user.models.EmailUser user: regular user

        """
        is_staff = extra_fields.pop("is_staff", False)
        return self._create_user(email, password, is_staff, False,
                                 **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save an EmailUser with the given email and password.

        :param str email: user email
        :param str password: user password
        :return custom_user.models.EmailUser user: admin user

        """
        return self._create_user(email, password, True, True,
                                 **extra_fields)


class User(AbstractBaseUser):
    email = models.EmailField('email address', max_length=255,
                              unique=True, db_index=True)
    alias = models.CharField(max_length=20)
    location = models.CharField(max_length=30, blank=True)
    is_staff = models.BooleanField('staff status', default=False,)
    is_active = models.BooleanField('active', default=True,)
    is_superuser = models.BooleanField('active', default=False,)
    date_joined = models.DateTimeField('date joined', default=datetime.datetime.now)

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ['password']

    objects = EmailUserManager()


class Message(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField(max_length=3000)
    message_html = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.message
