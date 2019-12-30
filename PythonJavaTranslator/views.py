from django.shortcuts import redirect


def redirect_view(request):
    response = redirect('/translator/')
    return response
