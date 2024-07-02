from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import render
from django.template.loader import render_to_string
from django.utils.html import strip_tags


def home(request):
    return render(request, 'landing/flat/home.html')
