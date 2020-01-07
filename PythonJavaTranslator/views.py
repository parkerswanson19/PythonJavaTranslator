from django.shortcuts import redirect
from django.shortcuts import render


def redirect_view(request):
    response = redirect('/translator/')
    return response


def aboutTheCreators(request):
    return render(request, 'aboutMe.html')
