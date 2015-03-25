import requests
from bs4 import BeautifulSoup
from pprint import pprint

class PokeScrapr(object):

    BASE_URL = "http://pokemondb.net/pokedex/{}/moves/1" 

    def __init__(self):
        '''Construct a new PokeScrapr. For now, the constructor takes no 
        arguments'''
        pass

    def get_moves(self, pokemon, moveset = "natural"):
        '''Returns a list of 2 element lists, corresponding to 
        level, move_name pairs.

        >>> scraper = PokeScrapr()
        >>> scraper.get_moves("bulbasaur", moveset = "natural")
        [['1', 'Growl'],
         ['1', 'Tackle'],
         ['7', 'Leech Seed'],
         ['13', 'Vine Whip'],
         ['20', 'Poison Powder'],
         ['27', 'Razor Leaf'],
         ['34', 'Growth'],
         ['41', 'Sleep Powder'],
         ['48', 'Solar Beam']]

        :param pokemon: The name of the pokemon to look up.
        :type pokemon: str.
        :param moveset: The moveset to look up (natural, tm, hm).
        :type moveset: str.
        :returns: list.
        
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
        pprint(Scraper.get_moves(pokemon, moveset = "natural"))
        print()








