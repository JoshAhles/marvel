from multiprocessing import context
from django.shortcuts import render

# Create your views here.
def index(request):
    context = {}
    return render(request, 'marvelProject/index.html', context)

def searchresults(request):
    context = {}
    return render(request, 'marvelProject/search-results.html', context)
    
def info(request):
    context = {}
    return render(request, 'marvelProject/info.html', context)