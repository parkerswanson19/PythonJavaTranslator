from django.shortcuts import render
from .models import *
import time

# Create your views here.
from receiveInput.models import InputtedCode


def RapAnalyzerHomePage(request):
    return render(request, 'rap-analyzer.html')


def RapAnalyzerAnalyze(request):
    # t0 = time.clock()
    # Creates a new Song object and assigns it to a local variable
    # 'content' is the name of the first textbox on the HTML page. It's telling Django to take the content of that box,
    # and assign it to the input field in the InputtedCode class
    if len(request.POST['song-name']) == 0 and len(request.POST['artist-name']) == 0 and len(request.POST['lyrics']) \
            == 0:
        return render(request, 'rap-analyzer.html')

    new_input = Song(request.POST['song-name'], request.POST['artist-name'], request.POST['lyrics'])

    new_input.analyze()

    # t1 = time.clock()
    # print("Time elapsed: ", t1 - t0)  # CPU seconds elapsed (floating point)

    dict_tops = {"top_sumner": order_by('reading_level_p'),"top_flesch": order_by('reading_level_f'),
                 "top_gunning": order_by('reading_level_g'), "top_drugs": order_by('drugs'),
                 "top_adlibs": order_by('adlibs'), "top_jewelry": order_by('jewelry')}

    # Re-renders the page and passes the InputtedCode object to the HTML file so the text boxes can be updated
    return render(request, 'rap-analyzer2.html', {'code': new_input, 'top_hits': dict_tops})
