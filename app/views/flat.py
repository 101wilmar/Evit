from django.shortcuts import render


def home(request):
    return render(request, 'app/flat/home.html')


