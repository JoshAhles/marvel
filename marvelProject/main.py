from marvelPy import Marvel
from keys import PUBLIC_KEY, PRIVATE_KEY

marvel = Marvel(PUBLIC_KEY = PUBLIC_KEY, 
            PRIVATE_KEY = PRIVATE_KEY) 

character = marvel.characters

requestedCharacter = character.all(name = {"Iron Man"})["data"]["results"]

heroName = requestedCharacter[0]["name"]
print(heroName)

heroDescription = requestedCharacter[0]["description"]
print(requestedCharacter[0]["description"])

heroImage = requestedCharacter[0]["thumbnail"]
print(requestedCharacter[0]["thumbnail"])

def superHeroData():
    superHero = dict();
    superHero['name'] = {heroName}
    superHero['description'] = {heroDescription}
    superHero['image'] = {heroImage}
    return superHero


# print(description)