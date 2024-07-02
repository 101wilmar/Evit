import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, reverse, get_object_or_404

from app.models import Subscription


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
    elif subscription_type == Subscription.TypeChoices.ANNUAL:
        end_datetime = now + datetime.timedelta(days=365)
    else:
        return redirect(reverse('app:home'))
    subscription = Subscription.objects.create(
        user=user,
        type=subscription_type,
        start_datetime=now,
        end_datetime=end_datetime
    )
    subscription.save()
    messages.success(request, 'Вы активировали подписку')
    return redirect(reverse('app:subscription_plans'))


@login_required
def remove_subscription(request, subscription_id):
    subscription = get_object_or_404(Subscription, id=subscription_id)
    subscription.delete()
    messages.error(request, 'Подписка отменена')
    return redirect(reverse('app:subscription_plans'))
