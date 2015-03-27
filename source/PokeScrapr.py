import requests
import json
import jsbeautifier
import sys
import time

from bs4 import BeautifulSoup
from pprint import pprint

## TODO fix eevee, magikarp, gloom, 

class PokeScrapr(object):
    '''Existing Pokemon APIs lack support for generation 1, so
    we're scraping the data instead. 
    '''

    BASE_POKEDEX_URL   = "http://pokemondb.net/pokedex/{}" 

    def __init__(self):
        '''Construct a new PokeScrapr. For now, the constructor takes no 
        arguments'''
        self.cache = {}
        self.r = None
        

    def _get_pokedex_soup(self, pokemon):
        '''We're going to need to scrape a bunch of information off each page in 
        the pokedex. Better to just make one HTTP request and pass the soup around.

        _get_pokedex_soup caches results in self.cache, so a call to
        get_evolution_sequence() followed by a call to get_pokedex_entry() 
        will still only take one HTTP request.
        '''
        if (pokemon in self.cache):
            return self.cache.get(pokemon)

        url  = self.BASE_POKEDEX_URL.format(pokemon)
        self.r    = requests.get(url)
        if not self.r.ok:
            sys.exit('bad request')
        soup =  BeautifulSoup(self.r.text)

        self.cache[pokemon] = soup
        return soup

    def get_moves(self, pokemon, moveset = "natural"):
        '''Returns a list of 2 element lists, corresponding to 
        level, move_name pairs.

        Unfortunately, since the moves for gen 1 are on a seperate page,
        we'll have to make a second HTTP request

        >>> scraper = PokeScrapr()
        >>> scraper.get_moves("bulbasaur", moveset = "natural")


        :param pokemon: The name of the pokemon to look up.
        :type pokemon: str.
        :param moveset: The moveset to look up (natural, tm, hm).
        :type moveset: str.
        :returns: list.
        
        '''

        url  = self.BASE_POKEDEX_URL.format(pokemon) + '/moves/1'
        r    = requests.get(url)
        soup = BeautifulSoup(r.text)

        tid = {
                 "natural" : 0,
                 "hm"      : 1,
                 "tm"      : 2
        }.get(moveset)

        # for whatever reason the website doesn't put in empty tables
        # in these cases
        if (pokemon.lower() in ('nidoran-f', 'nidoran-m')):
            tid = 1

        all_moves = []
        tables    = soup.find_all("table")

        # check for 'pre-evolution-moves' and skip them
        try:
            table = tables[tid]
            title = table.previous_sibling.previous_sibling.previous_sibling.previous_sibling
            if (title.text == 'Pre-evolution moves'):
                tid += 1

        except:
            return []

        # Some pokemon, like caterpie, have no hm/tm moves
        try:
            rows      = tables[tid].find_all('tr')
        except: 
            return []


        for row in rows:
            move = [e.text for e in row.find_all('td')]
            all_moves.append(move)

        # Each move is a 6-Tuple (level, move_name, type, category, power, accuracy)
        # If FSP ever requires more information than just the level and move_name, we 
        # can easily extend this    
        return [ move[:2] for move in all_moves if move ]


    def get_evolution_sequence(self, pokemon):
        ''' Returns an evolution sequence, where a 
        sequence is a list of [pokemon_name, evolution_mechanism, evolved_pokemon_name].

        TODO fix eevee (and other edge cases if they exist)

        :returns list: The evolution sequence
        '''

        soup = self._get_pokedex_soup(pokemon)
        try:
            sequence = soup.find_all('div', {'class': 'infocard-evo-list'})[0]

        # Some pokemon (like farfetchd) have no evolution sequence
        except:
            return [[pokemon, "Undefined", "Undefined"]]

        pokemon_sequence = sequence.find_all('span', {'class' : 'infocard-tall'})
        evolution_info = sequence.find_all('span', {'class' : 'infocard-tall small'})

        pokemon_names, evolution_mechanisms = [], []

        for p in pokemon_sequence:
            pokemon = p.find('a', {'class' : 'ent-name'})

            if pokemon:
                pokemon_names.append(pokemon.get('href').split('/')[-1].capitalize())

        for e in evolution_info:
            evolution_mechanisms.append(
                (e.br.text.strip().replace('(', '').replace(')', '')))

        evolution_mechanisms.append("Undefined")

        evolution_tuples = [[i,j] for i,j in zip(pokemon_names, evolution_mechanisms)]

        for i in range(len(evolution_tuples) - 1):
            evolution_tuples[i].append(pokemon_names[i+1])

        evolution_tuples[-1].append("Undefined")
        return evolution_tuples
            

    def get_pokedex_data(self, pokemon):
        soup = self._get_pokedex_soup(pokemon)
        table = soup.find_all('table')[0]
        rows = table.find_all('tr')
        pokedex_data = []

        for i,row in enumerate(rows):
            entry = None

            # national_id
            if i == 0:
                entry = row.find('td').text.strip()

            # type(s)
            elif i == 1:
                entry = row.find('td').text.strip().split()

            # species (pokemon suffix not included)
            elif i == 2:
                entry = ' '.join(row.find('td').text.strip().split()[:-1])

            # height [feet, inches]
            elif i == 3:
                entry = row.find('td').text.strip().split()[0].strip('″').split('′')

            # weight (lbs)
            elif i == 4: 
                entry = row.find('td').text.split()[0].strip()

            pokedex_data.append(entry)

        schema = ["national_id", "types", "species", "height", "weight"]
        return { i: j for i,j in zip(schema, pokedex_data) }

    def get_base_stats(self, pokemon):
        '''Returns the hp, attack, defense, special_attack, special_defense, 
        and speed of a pokemon.

        :param pokemon: The name of the pokmeon to look up.
        :type pokemon: str.
        '''
        soup = self._get_pokedex_soup(pokemon)
        table = soup.find_all('table')[3]
        rows = table.find_all('tr')

        schema = ["hp", "attack", "defense", "special_attack", "special_defense", "speed"]
        stats = [row.find('td').text for row in rows if row.find('td')]

        return { i:j for i,j in zip(schema, stats[1:]) }

    def get_pokedex_entry(self, pokemon):
        '''Returns the red/blue pokedex entry of a pokemon.
        THIS IS BUGGY

        :param pokemon: The name of the pokemon to look up.
        :type pokemon: str.
        :returns string:
        '''
        soup = self._get_pokedex_soup(pokemon)
        headings = soup.find(id='dex-flavor')
        table = headings.next_sibling.next_sibling.next_sibling.next_sibling
        

        # Gen 1 is the first entry in the table, so no need for a find_all here
        entry = table.tr.td.text
        return entry

    def _format_moveset_for_FSP(self, moveset):
        updated_moves = [ {"level" : int(m[0]), "Move": m[1]} for m in moveset]

        # quick hack to force double quotes instead of single quotes
        updated_moves = '{}'.format(updated_moves)
        updated_moves = jsbeautifier.beautify(updated_moves).replace("'", '"')               

        return updated_moves

    def get_all_data(self, pokemon):
        # Set up storage container.
        d = {}

        # name
        d['pokemon_name'] = pokemon

        # Scrape all the data
        pokedex_entry        = self.get_pokedex_entry(pokemon)
        pokedex_data         = self.get_pokedex_data(pokemon)
        evolution_sequence   = self.get_evolution_sequence(pokemon)
        base_stats           = self.get_base_stats(pokemon)
        natural_moves        = self.get_moves(pokemon, moveset = "natural")
        tm_moves             = self.get_moves(pokemon, moveset = "tm")
        hm_moves             = self.get_moves(pokemon, moveset = "hm")

        # national_id, types, species, height, weight
        for i in ['national_id', 'species', 'height', 'weight']:
            d[i] = pokedex_data[i]

        # break up height into feet, inches
        d['feet'] = d['height'][0]
        d['inches'] = d['height'][1]

        # force double quotes in types
        types = pokedex_data['types']
        for i in range(len(types)):
            types[i] = '"' + types[i] + '"'

        d['types'] = ','.join(types)

        # hp, attack, defense, special_attack, special_defense, speed
        for i in ['hp', 'attack', 'defense', 'special_attack',
                    'special_defense', 'speed']:
            d[i] = base_stats[i]

        # pokedex_entry
        d['pokedex_entry'] = pokedex_entry

        # evolution info
        found = False
        for subsequence in evolution_sequence:
            if subsequence[0] == pokemon:
                d["evolvesVia"]  = subsequence[1]
                d["evolvesInto"] = subsequence[2]
                found = True

        if not found:
            sys.exit('evolution data not found for {}. {}'.format(
                pokemon, evolution_sequence))
        #movesets
        natural_moves = self._format_moveset_for_FSP(natural_moves)
        tm_moves      = self._format_moveset_for_FSP(tm_moves)
        hm_moves      = self._format_moveset_for_FSP(hm_moves)

        d['natural_moves'] = natural_moves
        d['tm_moves']      = tm_moves
        d['hm_moves']      = hm_moves

        return d

    def get_FSP_JSON(self, pokemon):
        '''Returns a JSON formatted string compatible with math.js in 
        fullscreenpokemon.

        :param pokemon: The name of the pokemon to look up.
        :type pokemon: str.
        :returns string:
        '''

        pokemon = pokemon.capitalize()

        output = '''
        "{pokemon_name}": {{
            "label": "{species}",
            "sprite": "water",
            "info": [
                    "{pokedex_entry}"
            ]
            "evolvesInto" : "{evolvesInto}",
            "evolvesVia" : "{evolvesVia}",
            "number": {national_id},
            "height": ["{feet}", "{inches}"],
            "weight": {weight},
            "types": [{types}],
            "HP": {hp}, 
            "Attack": {attack}, 
            "Defense": {defense},
            "Special": {special_attack}, 
            "Speed": {speed}, 
            "moves": {{
                "natural": {natural_moves}, 
                "hm": {hm_moves},
                "tm": {tm_moves}
            }}
        }}
        '''

        kwargs = self.get_all_data(pokemon)
        output = output.format(**kwargs)
        return jsbeautifier.beautify(output)

if __name__ == '__main__':
    Scraper = PokeScrapr()

    
    for pokemon in ["Weepinbell"]:
        print(pokemon.upper())
        print(Scraper.get_FSP_JSON(pokemon))
        
    #pprint(Scraper.get_pokedex_data("pikachu"))
    #pprint(Scraper.get_FSP_JSON("squirtle"))
    #pprint(Scraper.get_base_stats("pikachu"))
    #print(Scraper.get_FSP_JSON("Venusaur"))
    #print(Scraper.get_pokedex_entry("charizard"))







