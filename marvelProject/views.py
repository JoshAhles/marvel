from multiprocessing import context
from django.http import HttpResponse
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.utils.datastructures import MultiValueDictKeyError
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

#home page
def index(request):
    context = {}
    return render(request, 'index.html', context)

#search result page
def searchresults(request):
    #receiving name from home page search input
    hero_name = request.GET['hero']
    #accessing API with keys
    marvel = Marvel(PUBLIC_KEY = PUBLIC_KEY, 
            PRIVATE_KEY = PRIVATE_KEY) 

    character = marvel.characters
    #calling API with the passed in name from home page
    requestedCharacter = character.all(name = {hero_name})["data"]["results"]

    #error handling, go back home if no character found
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

    #sending data to the HTML as Django variables to be accessible
    return render(request, 'searchresults.html', {'hero':hero_name, 'description':heroDescription, 'image':heroImage})
    
#info page, will fill in info on my project here    
def info(request):
    context = {}
    return render(request, 'info.html', context)


#authenticate the firebase (utilizing pyrebase to call on firebase implementation)
firebase = pyrebase.initialize_app(config)
authe = firebase.auth()
#all database data stored here 
database = firebase.database()


#add page (shows the add success message when adding hero (page that actually send the hero data to the firebase))
def add(request):
    #grabs the name of the hero upon button click (add hero from search results)
    heroAdded = request.GET['heroNameToAdd']
    #accessing the API
    marvel = Marvel(PUBLIC_KEY = PUBLIC_KEY, 
            PRIVATE_KEY = PRIVATE_KEY) 

    character = marvel.characters

    #using the name sent over to make a variable
    requestedCharacter = character.all(name = {heroAdded})["data"]["results"]

    #create URL from data received for image from API
    imageAdded = requestedCharacter[0]["thumbnail"]["path"]
    imageAdded += "."
    imageAdded += requestedCharacter[0]["thumbnail"]["extension"]

    data = {"Name": heroAdded, "Image": imageAdded}

    entry = heroAdded
    
    #actual storage implementation, stores Name under Heros Root, and then image under hero name
    database.child("Heros").child(entry).set(data)
    return render(request, 'add.html')

#delete page, shows success delete message (actual delete implementation occurs on visiting page)
def delete(request):
    #receiving the hero to remove from database, sent from the button click
    heroDelete = request.GET['heroNameToDelete']
    #removing the whole node for the particular Hero name
    database.child("Heros").child(heroDelete).remove()
    return render(request, 'delete.html')

#viewteam page that shows all the currently added heros in the firebase database
def viewteam(request):

    #setting up the data structures
    dicts = {}
    keysDb = [] 
    valuesDb = []

    #getting the actual stored values from database
    herosDb = database.child("Heros").get()

    #only proceeding if there is data to get 
    if herosDb.each() is not None: 
        #looping through the database records
        for heroIn in herosDb.each():
            #getting the dictionary containing the name and image of each record
            values = heroIn.val()
            #sending to the variables to pass to HTML page 
            keysDb.append(values["Name"])
            databaseHeroName = values["Name"]
            valuesDb.append(values["Image"])
            databaseHeroImage = values["Image"]
     
    #python loop through to add to the dictionary that I am sending to my HTML page
    for i in range(len(keysDb)):
        dicts[keysDb[i]] = valuesDb[i]
 
    #giving the dictionary just created as the context to send to HTML page
    context = {

        "data" : dicts

    }

    #convert the data retrieved into a dictionary, then access the dict from the page
    addedHeroName = database.child('Name').get().val
    addedHeroImage = database.child('Image').get().val

    return render(request, 'viewteam.html', context)


