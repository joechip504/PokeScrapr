import unittest
from PokeScrapr import PokeScrapr
from pprint import pprint

class TestPokeScrapr(unittest.TestCase):

    def setUp(self):
        self.Scrapr  = PokeScrapr()
        self.test_pokemon_1 = "bulbasaur"

    def test_constructor(self):
        self.assertEqual("<class 'PokeScrapr.PokeScrapr'>", 
               str(type(self.Scrapr)))

    def test_getMovesLearntByLevelUp(self):
        moves = self.Scrapr.getMoves(self.test_pokemon_1, moveset = "natural")
        pprint(moves)



if __name__ == '__main__':
    unittest.main()

