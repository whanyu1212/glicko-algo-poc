from .glicko_math import GlickoMath
from ..match.match_simulator import MatchSimulator
from glicko.player.team import Team


class GlickoRating:
    def __init__(self, team1: Team, team2: Team):
        self.team1 = team1
        self.team2 = team2
        self.outcome = MatchSimulator(team1, team2).simulate().winner

    def update_rating_stats(self):
        g = GlickoMath.calculate_g(self.team1.avg_rd)
        E = GlickoMath.calculate_E(g, self.team1.avg_rating, self.team2.avg_rating)
        v = GlickoMath.calculate_v(g, E)
        delta = GlickoMath.calculate_delta(v, g, self.outcome.value, E)
        new_sigma = GlickoMath.calculate_new_volatility(
            self.team1.avg_rd, self.team1.avg_rd, delta, v
        )
        phi_star = GlickoMath.calculate_new_deviation(
            self.team1.avg_rd, new_sigma, delta
        )
        new_phi = GlickoMath.calculate_new_phi(phi_star, new_sigma)

        new_mu = GlickoMath.calculate_new_rating(
            self.team1.avg_rating, new_phi, self.team1.avg_rd, delta
        )

        return new_mu, new_phi, new_sigma

    def update_player_rating(self):
        new_mu, new_phi, new_sigma = self.update_rating_stats()
        for player in self.team1.players:
            player["μ"] = player["μ"] + (new_mu - self.team1.avg_rating)
            player["φ"] = player["φ"] + (new_phi - self.team1.avg_rd)
            player["σ"] = player["σ"] + (new_sigma - self.team1.avg_sigma)
            player["R"] = 173.7178 * player["μ"] + 1500
            player["RD"] = 173.7178 * player["φ"]
