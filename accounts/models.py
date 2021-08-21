from django.contrib.auth.models import (AbstractUser)

from django.contrib.auth.models import (
    AbstractBaseUser,PermissionsMixin
)
from django.db import models
from django.contrib.auth.models import ( AbstractUser
)
from phonenumber_field.modelfields import PhoneNumberField
from django.utils.translation import gettext_lazy as _



class User(AbstractUser):
    username = models.CharField(
        max_length=64,
        verbose_name=_('Имя пользователя'),
        unique=True
    )
    first_name = models.CharField(
        _('Имя'),
        max_length=150
    )
    last_name = models.CharField(
        _('Фамилия'),
        max_length=150
    )
    phone_number = PhoneNumberField(verbose_name=_('Номер телефона'))

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    class Meta:
        ordering = ('username',)

    def __str__(self):
        return self.username

