from multiprocessing import context
from django.http import HttpResponse
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.utils.datastructures import MultiValueDictKeyError
# from marvel import Marvel
from marvel import Marvel
from marvelProject.keys import *
import requests
import json
import pyrebase

#setting up firebase config
#python dictionary
config={

    "apiKey": "AIzaSyDwOqINChKrC-YH0d9NEWFrNrQWqW65krg",
    "authDomain": "marvel-97d87.firebaseapp.com",
    "databaseURL": "https://marvel-97d87-default-rtdb.firebaseio.com",
    "projectId": "marvel-97d87",
    "storageBucket": "marvel-97d87.appspot.com",
    "messagingSenderId": "610646675959",
    "appId": "1:610646675959:web:9be",

}


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


#authenticate the firebase
firebase = pyrebase.initialize_app(config)
authe = firebase.auth()
#all database data stored here 
database = firebase.database()

countIt = 0

def viewteam(request):
    #all i need to push out is hero and image on button click from search result
    #for ease of implementation, should copy same logic for how I pull in the data to the search result from the first page
    # databaseAddHero = request.GET['heroNameToAdd']
    # databaseAddImage = request.GET['heroImageToAdd']
    # print(databaseAddHero)

    # addedHeroName = request.GET['heroNameToAdd']
    # marvel = Marvel(PUBLIC_KEY = PUBLIC_KEY, 
    #         PRIVATE_KEY = PRIVATE_KEY) 

    # character = marvel.characters
    heroAdded = request.GET['heroNameToAdd']


    marvel = Marvel(PUBLIC_KEY = PUBLIC_KEY, 
            PRIVATE_KEY = PRIVATE_KEY) 

    character = marvel.characters

    requestedCharacter = character.all(name = {heroAdded})["data"]["results"]

    imageAdded = requestedCharacter[0]["thumbnail"]["path"]
    imageAdded += "."
    imageAdded += requestedCharacter[0]["thumbnail"]["extension"]

    # requestedCharacter = character.all(name = {hero_name})["data"]["results"]

    data = {"Name": heroAdded, "Image": imageAdded}
    global countIt
    
    countIt = countIt + 1
    
    database.child("Heros").child(countIt).set(data)


    # inventory = datab.child("Inventories").get()
    # for business in inventory.each():
    #     print(business.val())

    # context = {
    #     "data" : [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
    # }



    herosDb = database.child("Heros").get()
    for heroIn in herosDb.each()[1:]:
        values = heroIn.val()
        print(values["Name"])
        # parser = json.loads(str(heroIn.val()))
        # print(parser["Name"])
        

    
 

        #convert the data retrieved into a dictionary, then access the dict from the page


    # all_users = database.child("Heros").child("Name").get()
    # for user in all_users.each():
    #     print(user.val()) # {name": "Mortimer 'Morty' Smith"}
 
    # database.child("Hero").child(heroNameToDelete).remove()
    #if coming from home page, don't send the data 

    addedHeroName = database.child('Name').get().val
    addedHeroImage = database.child('Image').get().val
    # return render(request, 'viewteam.html', {
    #     'addedHeroName':addedHeroName,
    #     "addedHeroImage":addedHeroImage
    # })
    return render(request, 'viewteam.html', {'addedHeroName':heroAdded, 'addedHeroImage':imageAdded})


    #on button click, reload page and delete selected hero
    #when coming from other page, add hero

