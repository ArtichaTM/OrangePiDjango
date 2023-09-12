from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse


class User(AbstractUser):
    username = models.CharField(max_length=20, unique=True, verbose_name='Имя пользователя')
    email = models.EmailField(max_length=40, unique=True, verbose_name='E-mail')
    name = models.CharField(max_length=50, default='User', verbose_name='ФИО')

    first_name = None
    last_name = None

    def uname(self) -> str:
        return self.username

    def url(self) -> str:
        return reverse('AuthApp:profile_username', kwargs={'target_user': self.id})

    def __str__(self) -> str:
        return self.username

    def __repr__(self):
        return str(self)
