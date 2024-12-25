from typing import Dict, List, Optional
from .models import Player
from .player_factory import PlayerFactory


class PlayerPool:
    def __init__(self, factory: PlayerFactory):
        """Initializes the PlayerPool with the given PlayerFactory class.

        Args:
            factory (PlayerFactory): a PlayerFactory object that creates players
        """
        self.factory = factory
        self.players: Dict[str, Player] = {}

    def generate_players(self, count: int) -> None:
        """Generate a number of players. Store the players in a dictionary
        with the player name as the key and the player object as the value.

        Args:
            count (int): _description_
        """
        for i in range(count):
            player = self.factory.create_player(i)
            self.players[player.name] = player

    def get_player(self, name: str) -> Optional[Player]:
        """Method to retrive a player from the player pool
        using the player's name.

        Args:
            name (str): the key to search for in the player pool

        Returns:
            Optional[Player]: the player object if found, otherwise None
        """
        return self.players.get(name, None)

    def get_all_players(self) -> List[Player]:
        """Method to retrieve all players from the player pool
        and store them in a list.

        Returns:
            List[Player]: list of Player objects
        """
        return list(self.players.values())
