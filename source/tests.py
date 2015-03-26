import unittest
from PokeScrapr import PokeScrapr
from pprint import pprint

class TestPokeScrapr(unittest.TestCase):

    def setUp(self):
        self.Scrapr  = PokeScrapr()
        self.test_pokemon_1 = "bulbasaur"

    def test_constructor(self):
        self.assertEqual(PokeScrapr, type(self.Scrapr))

    def test_natual_moves(self):
        moves = self.Scrapr.get_moves(self.test_pokemon_1, moveset = "natural")
        self.assertEqual('1', moves[0][0])
        self.assertEqual('Growl', moves[0][1])

    def test_hm_moves(self):
        moves = self.Scrapr.get_moves(self.test_pokemon_1, moveset = "hm")
        self.assertEqual('Cut', moves[0][1])

    def test_tm_moves(self):
        moves = self.Scrapr.get_moves(self.test_pokemon_1, moveset = "tm")
        self.assertEqual('3', moves[0][0])
        self.assertEqual('Swords Dance', moves[0][1])

if __name__ == '__main__':
    unittest.main()

