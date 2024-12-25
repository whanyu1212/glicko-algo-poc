from random import uniform
from .models import Player
from .config import PlayerRanges


class PlayerFactory:
    def __init__(self, ranges: PlayerRanges = PlayerRanges()):
        """Initializes the PlayerFactory with the given ranges.

        Args:
            ranges (PlayerRanges, optional):  Defaults to PlayerRanges().
        """
        self.ranges = ranges

    def create_player(self, player_id: int) -> Player:
        """Create a player with the fields preset in the Player dataclass
        and random values within the allowed ranges.

        Args:
            player_id (int): a random integer to identify the player

        Returns:
            Player: a Player object that contains the player's information
            such as name, rating, rating deviation, volatility, and mu, phi
        """
        R = uniform(self.ranges.r_min, self.ranges.r_max)
        RD = uniform(self.ranges.rd_min, self.ranges.rd_max)
        sigma = uniform(self.ranges.sigma_min, self.ranges.sigma_max)

        return Player(
            name=f"Player_{player_id}",
            R=R,
            RD=RD,
            σ=sigma,
            μ=(R - 1500) / self.ranges.glicko_constant,
            φ=RD / self.ranges.glicko_constant,
        )
