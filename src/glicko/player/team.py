from dataclasses import dataclass
from typing import List
from random import sample
from .player_pool import PlayerPool
from .models import Player


@dataclass
class Team:
    """Team with randomly sampled players."""

    team_id: str
    size: int = 5
    players: List[Player] = None

    def sample_players(self, player_pool: PlayerPool) -> None:
        """Forms team by sampling from player pool."""
        available_players = player_pool.get_all_players()
        if len(available_players) < self.size:
            raise ValueError(
                f"Not enough players. Need {self.size}, have {len(available_players)}"
            )

        self.players = sample(available_players, self.size)

    @property
    def avg_rating(self) -> float:
        if not self.players:
            raise ValueError("Team has no players")
        return sum(p.R for p in self.players) / self.size

    @property
    def avg_rd(self) -> float:
        if not self.players:
            raise ValueError("Team has no players")
        return sum(p.RD for p in self.players) / self.size


# Usage:
# pool = PlayerPool(factory)
# pool.generate_players(100)
# team = Team("Team_1")
# team.sample_players(pool)
# print(team.avg_rating)
