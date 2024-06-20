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

    # Referral
    path('referral', views.referral_list, name='referral_list'),

    # User Quiz
    path('quiz', views.quiz_list, name='quiz_list'),
    path('quiz/start', views.start_quiz, name='start_quiz'),
    path('quiz/save', views.save_quiz, name='save_quiz'),
    path('quiz/<int:user_quiz_id>', views.quiz_detail, name='quiz_detail'),

    # Quiz Management
    path('management-quiz', views.management_quiz_list, name='management_quiz_list'),
    path('management-quiz/<int:pk>', views.management_quiz_detail, name='management_quiz_detail'),
]
