from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.shortcuts import redirect, reverse, render

from app.models import Referral
from landing.forms.user import UserForm


def auth(request):
    referral_code = request.GET.get('referral-code')
    return render(request, 'landing/auth/auth.html', {
        'referral_code': referral_code
    })


def sign_in(request):
    if not request.method == 'POST':
        return redirect(reverse('landing:auth'))
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = authenticate(username=username, password=password)
    if user:
        print('logged in successfully')
        login(request, user)
        return redirect(reverse('app:cabinet'))
    print(username, password)
    print('Invalid username or password')
    return redirect(reverse('landing:auth'))


def sign_up(request):
    if request.method != 'POST':
        return redirect(reverse('landing:auth'))

    referral_code = request.GET.get('referral-code')
    form = UserForm(request.POST)
    if form.is_valid():
        password = request.POST.get('password')
        user = form.save(commit=False)
        user.username = form.cleaned_data['email']
        try:
            user.set_password(password)
            user.is_active = False
            user.save()
            user.profile.password = password
            print(password)
            print(user.profile)
            user.profile.save()
            messages.warning(request, 'Вам на почту отправлена ссылка для активации')
            # send_email()
            if referral_code:
                referral = Referral.objects.filter(code=referral_code).first()
                referral.referred_users.add(user)
        except:
            messages.warning(request, 'Данная почта уже зарегистрировона')
            return redirect(reverse('landing:auth'))
    return redirect(reverse('app:home'))
