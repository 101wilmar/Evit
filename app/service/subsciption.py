import datetime

from django.contrib.auth.models import User

from app.models import Subscription


def activate_year_subscription(user: User) -> bool:
    try:
        now = datetime.datetime.now()
        end_datetime = now + datetime.timedelta(days=365)
        subscription = Subscription.objects.create(
            user=user,
            type=Subscription.TypeChoices.ANNUAL,
            start_datetime=now,
            end_datetime=end_datetime
        )
        subscription.save()
        return True
    except:
        return False
