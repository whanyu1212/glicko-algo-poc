import unittest
from glicko.player.models import Player
from glicko.player.player_pool import PlayerPool
from glicko.player.player_factory import PlayerFactory
from glicko.player.config import PlayerRanges


class TestPlayerPool(unittest.TestCase):
    def setUp(self):
        self.ranges = PlayerRanges()
        self.factory = PlayerFactory(self.ranges)
        self.pool = PlayerPool(self.factory)

    def test_generate_players(self):
        self.pool.generate_players(5)
        self.assertEqual(len(self.pool.players), 5)
        for i in range(5):
            player_name = f"Player_{i}"
            self.assertIn(player_name, self.pool.players)
            player = self.pool.players[player_name]
            self.assertTrue(
                isinstance(player, Player)
            )  # Assuming Player class is available
            self.assertTrue(self.ranges.r_min <= player.R <= self.ranges.r_max)
            self.assertTrue(self.ranges.rd_min <= player.RD <= self.ranges.rd_max)
            self.assertTrue(self.ranges.sigma_min <= player.σ <= self.ranges.sigma_max)

    def test_get_player(self):
        self.pool.generate_players(2)
        player = self.pool.get_player("Player_0")
        self.assertIsNotNone(player)
        self.assertEqual(player.name, "Player_0")  # Add a specific assertion
        self.assertIsNone(self.pool.get_player("NonExistentPlayer"))

    def test_get_all_players(self):
        self.pool.generate_players(3)
        all_players = self.pool.get_all_players()
        self.assertEqual(len(all_players), 3)

        # Verify that all generated players are in the list
        for i in range(3):
            found = False
            for player in all_players:
                if player.name == f"Player_{i}":
                    found = True
                    break
            self.assertTrue(found, f"Player {i} not found in all_players list")
