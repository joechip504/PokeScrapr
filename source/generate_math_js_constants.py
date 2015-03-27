from PokeScrapr import PokeScrapr
import jsbeautifier
import time

## TODO JS beautifier
# TODO wrap this up nicely

scraper = PokeScrapr()


output = []

with open('pokemon.txt') as f:
	for line in f.readlines()[:]:
		pokemon = line.strip().capitalize()
		print(pokemon)
		
		try:
			js = scraper.get_FSP_JSON(pokemon)
			print(js)
			output.append(js)
			time.sleep(3)

		except:
			print("error - ", pokemon, ". sleeping for 5 sec")
			time.sleep(5)

			scraper = PokeScrapr()
			js = scraper.get_FSP_JSON(pokemon)
			print(js)
			output.append(js)	

with open('pokemon-js.js', 'w') as f:
	json = jsbeautifier.beautify(','.join(output))
	f.write(json)
