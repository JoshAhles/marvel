from multiprocessing import context
from django.http import HttpResponse
from django.shortcuts import render


# Create your views here.
def index(request):
    context = {}
    return render(request, 'index.html', context)

# def searchresults(request):
#   context = {}
#   system = request.POST.get('hero', None)
#   context['hero'] = hero
#   return render(request, 'marvelProject/search-results.html', context)

def searchresults(request):
    hero_name = request.GET['hero']
    return render(request, 'searchresults.html', {'hero':hero_name})
    
def info(request):
    context = {}
    return render(request, 'info.html', context)