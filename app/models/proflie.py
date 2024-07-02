import uuid

from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.crypto import get_random_string

from .base import BaseModel


class Referral(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='referral')
    code = models.CharField(max_length=20, unique=True)
    referred_users = models.ManyToManyField(User, related_name='referred_by', blank=True)

    class Meta:
        verbose_name = 'Реферальная система'
        verbose_name_plural = 'Реферальная система'

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = get_random_string(10)
        super().save(*args, **kwargs)


class Profile(BaseModel):
    class RoleChoices(models.TextChoices):
        ADMIN = 'admin', 'Администратор'
        USER = 'user', 'Пользователь'

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    patronymic = models.CharField(max_length=256, null=True, blank=True, verbose_name='Отчество')
    password = models.CharField(max_length=256, null=True, blank=True, verbose_name='Пароль')
    role = models.CharField(max_length=256, default=RoleChoices.USER, choices=RoleChoices.choices)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'

    def __str__(self):
        return f'Профиль ({self.get_role_display()}) "{self.user.username}"'

    @property
    def get_full_name(self):
        full_name = ''
        user = self.user
        if user.last_name:
            full_name += user.last_name + ' '
        if user.first_name:
            full_name += user.first_name + ' '
        if self.patronymic:
            full_name += f' {self.patronymic}'
        full_name = full_name.strip()
        return full_name


@receiver(post_save, sender=User)
def create_user_data(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        Referral.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_data(sender, instance, **kwargs):
    instance.profile.save()
    instance.referral.save()
