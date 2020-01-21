from django.shortcuts import render


# Create your views here.
def RapAnalyzerHomePage(request):
    return render(request, 'rap-analyzer.html')


def RapAnalyzerAnalyze(request):
    return render(request, 'rap-analyzer.html')
