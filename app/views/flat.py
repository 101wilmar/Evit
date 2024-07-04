from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.shortcuts import render
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from yookassa import Payment

from constants import DOMAIN


@login_required
def home(request):
    # from yookassa import Configuration, Payment
    #
    # Configuration.account_id = '413522'
    # Configuration.secret_key = 'test_SJH_u2rTGYZT6z4UgMc58tWN9p1MsyiOSC2S7H1nWgQ'
    #
    # payments = Payment.list().items
    # for index, payment in enumerate(payments, start=1):
    #     print(index, payment.id, payment.test, payment.amount.value, payment.paid)
    # print(payments)
    # payment = Payment.create({
    #     "amount": {
    #         "value": "2.00",
    #         "currency": "RUB"
    #     },
    #     "payment_method_data": {
    #         "type": "bank_card"
    #     },
    #     "confirmation": {
    #         "type": "redirect",
    #         "return_url": "https://www.example.com/return_url"
    #     },
    #     "description": "Заказ №72"
    # })
    # print(payment.__dict__)
    # print(payment.confirmation.confirmation_url)
    # print(payment)


    # template_name = 'app/email/activate.html'
    # html = render_to_string(
    #     template_name=template_name,
    #     context={
    #         'uuid': User.objects.last().profile.uuid,
    #         'domain': DOMAIN
    #     }
    # )
    # print(html)
    # plain_message = strip_tags(html)
    # send_mail(
    #     'Evit | Активация аккаунта',
    #     plain_message,
    #     'ansagankabdolla4@gmail.com',
    #     ['kabdolla.ansagan@mail.ru'],
    #     fail_silently=False,
    #     html_message=html
    # )
    return render(request, 'app/flat/home.html')
