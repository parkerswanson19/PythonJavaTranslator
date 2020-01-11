from django.shortcuts import redirect
from django.shortcuts import render


def redirect_view(request):
    response = redirect('/translator/')
    return response


def mainPage(request):
    return render(request, 'main-page.html')


def aboutTheCreators(request):
    return render(request, 'about-the-creators.html')
