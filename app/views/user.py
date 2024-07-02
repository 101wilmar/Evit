from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, reverse, get_object_or_404

from app.forms.user import UserUpdateForm, ProfileUpdateForm
from app.models import Profile
from constants import DOMAIN


@login_required
def cabinet(request):
    return render(request, 'app/user/cabinet.html', {
        'user': request.user,
        'domain': DOMAIN
    })


@login_required
def update_user(request):
    if request.method != 'POST':
        return redirect(reverse('app:cabinet'))

    user = request.user
    user_form = UserUpdateForm(request.POST, instance=user)
    if user_form.is_valid():
        messages.success(request, 'Данные успешно изменены')
        user_form.save()
    else:
        messages.error(request, 'При обработке произошла ошибка, попробуйте позже')

    profile_form = ProfileUpdateForm(request.POST, instance=user.profile)
    if profile_form.is_valid():
        profile_form.save()

    return redirect(reverse('app:cabinet'))


def email_verify_user(request, uuid):
    user = get_object_or_404(User, profile__uuid=uuid)
    user.is_active = True
    user.save()
    messages.success(request, 'Вы активировали свою учетную запись, введите почту и пароль для входа в аккаунт')
    return redirect(reverse('landing:auth'))


@login_required
def verify_user(request, uuid):
    profile = get_object_or_404(Profile, uuid=uuid)
    user = profile.user
    user.is_active = True
    user.save()
    messages.success(request, f'Пользователь "{user.username}" активирован')
    return redirect(reverse('app:user_list'))


@login_required
def unverify_user(request, uuid):
    profile = get_object_or_404(Profile, uuid=uuid)
    user = profile.user
    user.is_active = False
    user.save()
    messages.success(request, f'Пользователь "{user.username}" деактивирован')
    return redirect(reverse('app:user_list'))


@login_required
def user_list(request):
    users = User.objects.all().order_by('-pk')
    return render(request, 'app/user/list.html', {
        'users': users
    })
