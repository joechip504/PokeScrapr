from bs4 import BeautifulSoup
import requests as r

with open('pokemon.txt', 'w') as f:
	url = 'http://pokemondb.net/pokedex/game/firered-leafgreen'
	soup = BeautifulSoup(r.get(url).text)
	all_pokemon = soup.find('div', {'class' : 'infocard-tall-list'})
	for p in all_pokemon.find_all('span', {'infocard-tall'}):
		link = p.find('a', {'class' : 'ent-name'}).get('href').split('/')[-1]
		f.write(link + '\n')