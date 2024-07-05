from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, reverse, get_object_or_404
from yookassa import Payment

from app.models import SubscriptionPayment, Profile


@login_required
def payment_list(request):
    if not request.user.profile.role == Profile.RoleChoices.ADMIN:
        messages.error(request, 'У вас недостаточно прав для просмотра данной страницы')
        return redirect(reverse('app:home'))
    subscription_payments = SubscriptionPayment.objects.filter(is_paid=True)
    return render(request, 'app/payment/list.html', {
        'subscription_payments': subscription_payments,
    })


@login_required
def payment_detail(request, yookassa_id):
    subscription_payment = get_object_or_404(SubscriptionPayment, yookassa_id=yookassa_id)
    return render(request, 'app/payment/status.html', {
        'subscription_payment': subscription_payment
    })
