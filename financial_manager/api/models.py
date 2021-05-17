from datetime import date
from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser

from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField('email', unique=True)
    first_name = models.CharField('name', max_length=30, blank=True)
    last_name = models.CharField('surname', max_length=30, blank=True)
    is_active = models.BooleanField('is_active', default=True)
    is_staff = models.BooleanField('staff status', default=False,)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('is_staff',)


class Transaction(models.Model):
    """ A model of transaction, related to User. """

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transactions')
    amount = models.FloatField(verbose_name='Sum of the transaction')
    date = models.DateField(default=date.today)

    def __str__(self):
        return f'{self.date} - {self.amount}'

    class Meta:
        ordering = ('-date',)
