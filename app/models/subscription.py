from django.contrib.auth.models import User
from django.db import models

from app.models import BaseModel


class Subscription(BaseModel):
    class TypeChoices(models.TextChoices):
        MONTHLY = 'monthly', 'Ежемесячная'
        ANNUAL = 'annual', 'Ежегодная'

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subscriptions')
    type = models.CharField(max_length=50, choices=TypeChoices.choices, default=TypeChoices.MONTHLY, verbose_name='Тип')
    start_datetime = models.DateTimeField(null=True, blank=True)
    end_datetime = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписка'

    def __str__(self):
        return f'{self.user.username} - {self.type}'


class Payment(BaseModel):
    subscription = models.ForeignKey(Subscription, on_delete=models.CASCADE, null=True, blank=True,
                                     related_name='payments')
    yokassa_id = models.CharField(max_length=50, null=True, blank=True, unique=True)
    amount = models.IntegerField(null=True, blank=True)
    is_paid = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Оплата YooKassa'
        verbose_name_plural = 'Оплаты YooKassa'

    def __str__(self):
        return self.yokassa_id
