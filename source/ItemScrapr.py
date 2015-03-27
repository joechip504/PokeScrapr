from bs4 import BeautifulSoup

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

	def get_items(self, tid, schema, category = 'main'):

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


if __name__ == '__main__':
	scraper = ItemScrapr()
	tid = 1
	schema = ['name', 'price', 'effect']
	scraper.get_items(tid, schema, category = 'main')

