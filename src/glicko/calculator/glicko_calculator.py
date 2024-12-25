from glicko.player.team import Team


class GlickoCalculator:
    def __init__(self, team1: Team, team2: Team, outcome: str):
        self.team1 = team1
        self.team2 = team2
        self.outcome = outcome
