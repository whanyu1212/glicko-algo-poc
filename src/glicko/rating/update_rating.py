from .glicko_math import GlickoMath
from ..match.match_simulator import MatchSimulator
from glicko.player.team import Team


class GlickoRating:
    def __init__(self, team1: Team, team2: Team):
        self.team1 = team1
        self.team2 = team2
        self.outcome = MatchSimulator(team1, team2).simulate().winner

    def update_ratings(self):
        g = GlickoMath.calculate_g(self.team1.avg_rd)
        E = GlickoMath.calculate_E(g, self.team1.avg_rating, self.team2.avg_rating)
        v = GlickoMath.calculate_v(g, E)
        delta = GlickoMath.calculate_delta(v, g, self.outcome.value, E)
        new_volatility = GlickoMath.calculate_new_volatility(
            self.team1.avg_rd, self.team1.avg_rd, delta, v
        )
        phi_star = GlickoMath.calculate_new_deviation(
            self.team1.avg_rd, new_volatility, delta
        )
