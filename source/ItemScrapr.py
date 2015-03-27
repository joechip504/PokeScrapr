from bs4 import BeautifulSoup
from jsbeautifier import beautify

class Item(object):
	'''Represents an item in Pokemon Blue.

	An item can have up to 4 attributes. 
		self.name      The name of the item. All items have this.
		self.price     The price of the item. Not required for all items.
		self.effect    The description of the item. All items have this.

		category        'main', 'key', or 'pokeball. All items have one
							of these 3 flagas set true.
	'''
	def __init__(self, **kwargs):
		self.name     = None
		self.price    = None
		self.effect   = None

		self.main     = False
		self.key      = False
		self.pokeball = False

		# Determine the category
		if kwargs.get('main'):
			self.main      = True
		elif kwargs.get('key'):
			self.key       = True
		elif kwargs.get('pokeball'):
			self.pokeball  = True

		# If there's a price, add it in
		price = kwargs.get('price')
		if price:
			self.price = int(price.replace('-', '0'))

		# Name and effect are required
		self.name   = kwargs.get('name')
		self.effect = kwargs.get('effect')

	def __repr__(self):
		return self.name

	def FSP_JSON(self):
		output = None
		kwargs = {'name' : self.name, 'price': self.price, 'effect': self.effect}
		if (self.price):
			output = '''{{
					"name" : "{name}",
					"price" : "{price}",
					"effect" : "{effect}"
					}}
					'''

		else:
			output = '''
					"name" : "{name}",
					"effect" : "{effect}"
					'''
		output = output.format(**kwargs)
		return beautify(output)

class ItemScrapr(object):
	'''ItemScrapr is designed to show us: 

	1. What are all the different items in Pokemon Blue?
		"main"      items 
		"key"       items
		"pokeball"  items 

		""

	2. Which Marts sell which items?

	Again, output should be something that FullScreenPokemon can accept.
	'''

	def __init__(self):

		# http://www.psypokes.com/rby/items.php
		# On March 27, 2015
		soup = BeautifulSoup(open('static/rby_item_list.html'))
		self.tables = soup.find_all('table', {'class': 'psypoke'})

		'''
		self.main_items      = tables[0]
		self.pokeball_items  = tables[1]
		self.key_items       = tables[2]
		'''

	def _get_items(self, tid, schema, category = 'main'):

		# Actual item data starts 2 rows in, so just trim those off here
		rows = self.tables[tid].find_all('tr')[2:]

		items = []

		for row in rows:
			item = row.find_all('td')
			
			attributes = [] 
			for attr in item:
				attributes.append(attr.string)
			
			kwargs = dict(zip(schema, attributes))
			kwargs[category] = True
			
			i = Item(**kwargs)
			items.append(i)

		return items

	def get_main_items(self):
		schema = ['name', 'price', 'effect']
		return self._get_items(0, schema, category = 'main')

	def get_pokeball_items(self):
		schema = ['name', 'price', 'effect']
		return self._get_items(1, schema, category = 'pokeball')

	def get_key_items(self):
		schema = ['name', 'effect']
		return self._get_items(2, schema, category = 'key')

if __name__ == '__main__':
	scraper = ItemScrapr()
	key_items = scraper.get_main_items()
	print(','.join([k.FSP_JSON() for k in key_items]))
