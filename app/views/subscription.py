import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, reverse, get_object_or_404

from app.models import Subscription, SubscriptionPayment

from yookassa import Configuration, Payment

from constants import DOMAIN

Configuration.account_id = '413522'
Configuration.secret_key = 'test_SJH_u2rTGYZT6z4UgMc58tWN9p1MsyiOSC2S7H1nWgQ'


@login_required
def subscription_plans(request):
    user = request.user
    now = datetime.datetime.now()
    active_subscriptions = user.subscriptions.filter(
        start_datetime__lte=now,
        end_datetime__gte=now
    )
    return render(request, 'app/subscription/plans.html', {
        'active_subscriptions': active_subscriptions
    })


@login_required
def activate_subscription(request):
    user = request.user
    subscription_type = request.GET.get('type')

    now = datetime.datetime.now()
    if subscription_type == Subscription.TypeChoices.MONTHLY:
        end_datetime = now + datetime.timedelta(days=30)
        amount = 299
        payment = Payment.create({
            "amount": {
                "value": f"{amount}",
                "currency": "RUB"
            },
            "payment_method_data": {
                "type": "bank_card"
            },
            "confirmation": {
                "type": "redirect",
                "return_url": f"{DOMAIN}{reverse('app:subscription_plans')}",
            },
            "description": "Месячная подписка"
        })
        yokassa_id = payment.id
        url = payment.confirmation.confirmation_url
    elif subscription_type == Subscription.TypeChoices.ANNUAL:
        end_datetime = now + datetime.timedelta(days=365)
        amount = 2990
        payment = Payment.create({
            "amount": {
                "value": f"{amount}",
                "currency": "RUB"
            },
            "payment_method_data": {
                "type": "bank_card"
            },
            "confirmation": {
                "type": "redirect",
                "return_url": f"{DOMAIN}{reverse('app:subscription_plans')}"
            },
            "description": "Годовая подписка"
        })

        yokassa_id = payment.id
        url = payment.confirmation.confirmation_url
    else:
        return redirect(reverse('app:home'))

    subscription = Subscription.objects.create(
        user=user,
        type=subscription_type,
        start_datetime=now,
        end_datetime=end_datetime
    )
    subscription.save()

    subscription_payment = SubscriptionPayment.objects.create(
        subscription=subscription,
        yookassa_id=yokassa_id,
        amount=amount
    )
    subscription_payment.save()

    messages.success(request, 'Вы активировали подписку')
    if url:
        return redirect(url)
    # return redirect(reverse('app:subscription_plans'))


@login_required
def remove_subscription(request, subscription_id):
    subscription = get_object_or_404(Subscription, id=subscription_id)
    subscription.delete()
    messages.error(request, 'Подписка отменена')
    return redirect(reverse('app:subscription_plans'))
