from PokeScrapr import PokeScrapr
import time

## TODO JS beautifier
# TODO wrap this up nicely

scraper = PokeScrapr()

errors = open('error-pokemon.txt', 'w')

with open('pokemon.txt') as f:
	for line in f.readlines()[128:]:
		pokemon = line.strip().capitalize()
		print(pokemon)
		
		try:
			print(scraper.get_FSP_JSON(pokemon))
			time.sleep(1)

		except:
			print("error - ", pokemon, ". sleeping for 5 sec")
			time.sleep(5)
			scraper = PokeScrapr()
			print(scraper.get_FSP_JSON(pokemon))
		