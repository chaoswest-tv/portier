from django.shortcuts import render

# Create your views here.

def index(request):
    # do fancy stuff here maybe
    return render(request, 'portal/index.html')
