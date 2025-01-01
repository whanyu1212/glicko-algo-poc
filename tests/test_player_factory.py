import unittest
from glicko.player.config import PlayerRanges
from glicko.player.player_factory import PlayerFactory


class TestPlayerFactory(unittest.TestCase):
    def setUp(self):
        self.ranges = PlayerRanges()
        self.factory = PlayerFactory(self.ranges)

    def test_init(self):
        self.assertEqual(self.factory.ranges, self.ranges)

    def test_create_player(self):
        player = self.factory.create_player(1)
        self.assertEqual(player.name, "Player_1")
        self.assertTrue(self.ranges.r_min <= player.R <= self.ranges.r_max)
        self.assertTrue(self.ranges.rd_min <= player.RD <= self.ranges.rd_max)
        self.assertTrue(self.ranges.sigma_min <= player.σ <= self.ranges.sigma_max)
        self.assertEqual(player.μ, (player.R - 1500) / self.ranges.glicko_constant)
        self.assertEqual(player.φ, player.RD / self.ranges.glicko_constant)
