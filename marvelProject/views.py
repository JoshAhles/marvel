from multiprocessing import context
from django.http import HttpResponse
from django.shortcuts import render
from django.http import HttpResponseRedirect
# from marvel import Marvel
from marvel import Marvel
from marvelProject.keys import *
import requests


# Create your views here.
def index(request):
    context = {}
    return render(request, 'index.html', context)

def searchresults(request):
    hero_name = request.GET['hero']
    marvel = Marvel(PUBLIC_KEY = PUBLIC_KEY, 
            PRIVATE_KEY = PRIVATE_KEY) 

    character = marvel.characters

    requestedCharacter = character.all(name = {hero_name})["data"]["results"]

    # heroName = requestedCharacter[0]["name"]

    # heroDescription = requestedCharacter[0]["description"]

    #error handling for character search
    try :
        heroName = requestedCharacter[0]["name"]
    except IndexError:
        hero_name = "INVALID"
        return HttpResponseRedirect("/")

    try :
        heroDescription = requestedCharacter[0]["description"]
    except IndexError:
        heroDescription = ""

    try :
        heroImage = requestedCharacter[0]["thumbnail"]["path"]
        heroImage += "."
        heroImage += requestedCharacter[0]["thumbnail"]["extension"]
    except IndexError:
        heroImage = ""


    # print(heroImage)

    # def superHeroData():
    #     superHero = dict();
    #     superHero['name'] = {heroName}
    #     superHero['description'] = {heroDescription}
    #     superHero['image'] = {heroImage}
    #     return superHero

    return render(request, 'searchresults.html', {'hero':hero_name, 'description':heroDescription, 'image':heroImage})
    
def info(request):
    context = {}
    return render(request, 'info.html', context)






