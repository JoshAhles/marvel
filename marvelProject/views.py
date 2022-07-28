from multiprocessing import context
from django.http import HttpResponse
from django.shortcuts import render
import requests


# Create your views here.
def index(request):
    context = {}
    return render(request, 'index.html', context)

def searchresults(request):
    hero_name = request.GET['hero']
    #doesn't properly call yet (looking into django secret keys before commiting)
    response = requests.get('https://gateway.marvel.com/').json()
    return render(request, 'searchresults.html', {'hero':hero_name, 'response':response})
    
    
def info(request):
    context = {}
    return render(request, 'info.html', context)






