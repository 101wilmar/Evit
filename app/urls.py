from django.urls import path
from . import views

app_name = 'app'
urlpatterns = [
    # Flat pages
    path('home', views.home, name='home'),
    path('cabinet', views.cabinet, name='cabinet'),
    path('statistic', views.statistic, name='statistic'),
    path('cabinet/update', views.update_user, name='update_user'),

    # User
    path('user', views.user_list, name='user_list'),
    path('user/<uuid:uuid>/verify', views.verify_user, name='verify_user'),
    path('user/<uuid:uuid>/unverify', views.unverify_user, name='unverify_user'),

    path('user/email-verify/<uuid:uuid>', views.email_verify_user, name='email_verify_user'),

    # Referral
    path('referral', views.referral_list, name='referral_list'),

    # User Quiz for admin
    path('user-quizzes', views.user_quiz_list, name='user_quiz_list'),

    # User Quiz
    path('quiz', views.quiz_list, name='quiz_list'),
    path('start-quiz', views.start_quiz, name='start_quiz'),
    path('quiz/save', views.save_quiz, name='save_quiz'),
    path('quiz/<int:user_quiz_id>', views.quiz_detail, name='quiz_detail'),
    path('quiz/<int:user_quiz_id>/recommendation', views.user_quiz_recommendation, name='user_quiz_recommendation'),
    path('quiz/<int:user_quiz_id>/recommendation/send', views.user_quiz_recommendation_send,
         name='user_quiz_recommendation_send'),
    path('quiz/<int:user_quiz_id>/recommendation/pdf', views.user_quiz_recommendation_pdf,
         name='user_quiz_recommendation_pdf'),

    # Subscription
    path('subscription', views.subscription_plans, name='subscription_plans'),
    path('subscription/activate', views.activate_subscription, name='activate_subscription'),
    # REFACTOR
    path('subscription/<int:subscription_id>/remove', views.remove_subscription, name='remove_subscription'),

    # PaymentSubscription
    path('payment', views.payment_list, name='payment_list'),
    path('payment/<str:yookassa_id>', views.payment_detail, name='payment_detail'),

    # Quiz Management
    path('management-quiz', views.management_quiz_list, name='management_quiz_list'),
    path('management-quiz/<int:pk>', views.management_quiz_detail, name='management_quiz_detail'),
]
