from django.shortcuts import render


def home(request):
    return render(request, 'landing/flat/home.html')
