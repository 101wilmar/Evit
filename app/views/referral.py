from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from app.models import Referral
from constants import DOMAIN
from app.models import Profile
from app.views.user_quiz import get_active_subscriptions_exists

@login_required
def referral_list(request):
    user = request.user
    referred_users = user.referral.referred_users.all()
    count = 5 - referred_users.count()
    count = 0 if count < 0 else count
    is_active_subscriptions = get_active_subscriptions_exists(request.user)
    role = request.user.profile.role


    return render(request, 'app/referral/list.html', {
        'admin_role': Profile.RoleChoices.ADMIN.value,
        'is_active_subscriptions': is_active_subscriptions,
        'role': role,
        'referred_users': referred_users,
        'domain': DOMAIN,
        'count': count
    })
