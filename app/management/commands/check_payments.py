import datetime

from django.core.management import BaseCommand
from django.utils import timezone
from yookassa import Payment

from app.models import SubscriptionPayment


class Command(BaseCommand):
    help = 'Скрипт для проверки на наличие новых оплат'

    # Refactor
    def handle(self, *args, **options):
        current_datetime = timezone.now()
        past_datetime = current_datetime - datetime.timedelta(hours=1)
        # print(past_datetime.time())
        subscription_payments = SubscriptionPayment.objects.filter(created_at__gt=past_datetime, is_paid=False)
        # print(subscription_payments.values_list('created_at'))
        for subscription_payment in subscription_payments:
            payment_id = subscription_payment.yookassa_id
            payment = Payment.find_one(payment_id)
            # print(payment.status)
            # print(payment.paid)
            if payment.paid:
                subscription_payment.is_paid = True
                subscription_payment.save()
