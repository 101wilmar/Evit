from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.shortcuts import render


@login_required
def home(request):
    # send_mail(
    #     'Evit | Активация аккаунта',
    #     '12',
    #     'e-vit@report.me',
    #     'ansagankabdolla4@gmail.com',
    # ['ansagankabdolla4@gmail.com'],
    # fail_silently=False,
    # html_message=html
    # )

    # payments = Payment.list().items
    # for index, payment in enumerate(payments, start=1):
    #     print(index, payment.id, payment.test, payment.amount.value, payment.paid)
    # print(payments)
    #
    #
    # print(payment.__dict__)
    # print(payment.confirmation.confirmation_url)
    # print(payment)

    # template_name = 'app/email/activate.html'
    # html = render_to_string(
    #     template_name=template_name,
    #     context={
    #         'uuid': User.objects.last().profile.uuid,F
    #         'domain': DOMAIN
    #     }
    # )
    # plain_message = strip_tags(html)
    # send_mail(
    #     'Evit | Активация аккаунта',
    #     plain_message,
    #     'e-vit@report.me',
    #     ['kabdolla.ansagan@mail.ru'],
    #     fail_silently=False,
    #     html_message=html
    # )
    return render(request, 'app/flat/home.html')
