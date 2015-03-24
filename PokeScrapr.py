import requests
from bs4 import BeautifulSoup
from pprint import pprint

class PokeScrapr(object):

    BASE_URL = "http://pokemondb.net/pokedex/{}/moves/1" 

    def __init__(self):
        ''' maybe pass in a list of pokemon to scrape '''
        pass

    def getMoves(self, pokemon, moveset = "natural"):
        '''
        Can pass in "natural, hm, or tm"
        '''

        url  = self.BASE_URL.format(pokemon)
        r    = requests.get(url)
        soup = BeautifulSoup(r.text)

        tid = {
                 "natural" : 0,
                 "hm"      : 1,
                 "tm"      : 2
        }.get(moveset)

        all_moves = []
        tables    = soup.find_all("table")
        rows      = tables[tid].find_all('tr')


        for row in rows:
            move = [e.text for e in row.find_all('td')]
            all_moves.append(move)

        # Each move is a 6-Tuple (level, move_name, type, category, power, accuracy)
        # If FSP ever requires more information than just the level and move_name, we 
        # can easily extend this    
        return [ move[:2] for move in all_moves if move ]


if __name__ == '__main__':
    Scraper = PokeScrapr()
    for pokemon in ["bulbasaur", "squirtle", "charmander"]:
        print(pokemon.upper())
        pprint(Scraper.getMoves(pokemon, moveset = "tm"))
        print()








