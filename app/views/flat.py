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


    # payments = Payment.list().items
    # for index, payment in enumerate(payments, start=1):
    #     print(index, payment.id, payment.test, payment.amount.value, payment.paid)
    # print(payments)


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
