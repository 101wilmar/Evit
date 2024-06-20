from django.shortcuts import render


def statistic(request):
    return render(request, 'app/flat/statistic.html')
