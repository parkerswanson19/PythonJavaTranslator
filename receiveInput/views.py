from django.shortcuts import render
from django.http import HttpResponseRedirect

from .models import InputtedCode
import os

print(os.getcwd())


# This method is called the first time the page is loaded. It just renders out the HTML file
def homePage(request):
    return render(request, 'fancyTemplate.html')


# This method is called every time the translate button is pressed
def takeInput(request):
    # Creates a new InputtedCode object and assigns it to a local variable
    # 'content' is the name of the first textbox on the HTML page. It's telling Django to take the content of that box,
    # and assign it to the input field in the InputtedCode class
    new_input = InputtedCode(input=request.POST['content'])

    new_input.translate()

    # Re-renders the page and passes the InputtedCode object to the HTML file so the text boxes can be updated
    return render(request, 'fancyTemplate.html', {'code': new_input})
