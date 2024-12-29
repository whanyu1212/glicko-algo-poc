from dataclasses import dataclass
import math
import random
from enum import Enum
from glicko.player.team import Team
from glicko.player.config import PlayerRanges


class MatchOutcome(Enum):
    TEAM1_WIN = 1
    TEAM2_WIN = 0


@dataclass
class MatchResult:
    winner: MatchOutcome
    win_probability: float
    rating_difference: float
    uncertainty: float


class MatchSimulator:
    def __init__(self, team1: Team, team2: Team):
        """Initialize match simulator with two teams.

        Args:
            team1 (Team): Team object representing first team.
            team2 (Team): Team object representing second team.
        """
        self.team1 = team1
        self.team2 = team2
        self.scaling_factor = PlayerRanges.glicko_constant
        self.normalizer = PlayerRanges.rd_max

    def calculate_win_probability(self) -> float:
        """Suppose we take team 1 as the reference team. Calculate the win probability of team 1.

        Returns:
            float: win probability of team 1.
        """
        rating_diff = self.team1.avg_rating - self.team2.avg_rating
        return 1 / (1 + math.exp(-rating_diff / self.scaling_factor))

    def calculate_uncertainty(self) -> float:
        """Calculate the uncertainty of the outcome based on the square root of the sum of the squares of the ratings deviation of the two teams.
        Returns:
            float: uncertainty of the outcome.
        """
        return math.sqrt(self.team1.avg_rd**2 + self.team2.avg_rd**2)

    def simulate(self) -> MatchResult:
        """Simulate the match outcome by executing the following steps:
        1. Calculate the win probability of team 1.
        2. Calculate the uncertainty of the outcome.
        3. Calculate the rating difference between the two teams.
        4. Adjust the win probability by the uncertainty.
        5. Generate a random number between 0 and 1.
        6. Return the match result based on the adjusted win probability.

        Returns:
            MatchResult: Enum representing the match outcome.
        """
        win_prob = self.calculate_win_probability()
        uncertainty = self.calculate_uncertainty()
        rating_diff = self.team1.avg_rating - self.team2.avg_rating
        adjusted_prob = win_prob * (1 - uncertainty / self.normalizer)

        outcome = (
            MatchOutcome.TEAM1_WIN
            if random.random() < adjusted_prob
            else MatchOutcome.TEAM2_WIN
        )

        return MatchResult(
            winner=outcome,
            win_probability=win_prob,
            rating_difference=rating_diff,
            uncertainty=uncertainty,
        )
