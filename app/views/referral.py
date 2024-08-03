from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from app.models import Referral
from constants import DOMAIN


@login_required
def referral_list(request):
    user = request.user
    referred_users = user.referral.referred_users.all()
    count = 5 - referred_users.count()
    count = 0 if count < 0 else count
    return render(request, 'app/referral/list.html', {
        'referred_users': referred_users,
        'domain': DOMAIN,
        'count': count
    })
