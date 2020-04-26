from django.shortcuts import render


def index(request):
    # do fancy stuff here maybe
    return render(request, 'portal/index.html')
