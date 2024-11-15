from models.pokemon import Pokemon, Team
import random
from attack import stat_modifier_multiplier, attack
from logger import logger


class Battle:

    victories = {}
    attacks_first = None
    attacks_second = None

    def __init__(self, team1: Team, team2: Team):
        self.team1 = team1
        self.team2 = team2
        self.battle_name = f"{team1.name}_vs_{team2.name}"

    def fight(self):
        # This function will simulate a battle between two teams of pokemons
        # The battle will end when one of the teams has no pokemons left
        # The function will return the winning team
        while not self.team1.is_defeated() and not self.team2.is_defeated():
            # The battle will be turn-based
            # Each turn, the fastest pokemon will attack
            # If two pokemons have the same speed, a random pokemon will attack first
            # The attacking pokemon will use a random move
            # The defending pokemon will receive damage
            # If the defending pokemon has no HP left, it will be removed from the team
            # The battle will end when one of the teams has no pokemons left
            t1_pokemon = self.team1.get_pokemon()
            t2_pokemon = self.team2.get_pokemon()
            first_attacker, second_attacker = self.get_fight_order(
                t1_pokemon, t2_pokemon
            )
            first_move = self.attacks_first.move_selector(first_attacker, second_attacker)
            attack_message = attack(first_move, first_attacker, second_attacker)
            logger.info(f"{self.battle_name}: {attack_message}")
            if second_attacker.is_alive():
                second_move = self.attacks_second.move_selector(second_attacker, first_attacker)
                attack_message = attack(second_move, second_attacker, first_attacker)
                logger.info(f"{self.battle_name}: {attack_message}")
            status = f"First attacker has {first_attacker.hp} HP left, second attacker has {second_attacker.hp} HP left"
            logger.info(f"{self.battle_name}: {status}")
            logger.info(
                f"{self.battle_name}: Team 1 has {self.team1.count_alive_pokemons()} pokemons left"
            )
            logger.info(
                f"{self.battle_name}: Team 2 has {self.team2.count_alive_pokemons()} pokemons left"
            )
        return self.team1 if not self.team1.is_defeated() else self.team2

    def best_of_n(self, n: int = 10):
        self.victories = {self.team1.name: 0, self.team2.name: 0}
        for i in range(n):
            winner = self.fight()
            self.victories[winner.name] += 1
            self.team1.reset_team()
            self.team2.reset_team()

    def save_results(self, path: str):
        output_file = f"{path}/{self.battle_name}.csv"
        with open(output_file, mode="w", newline="") as file:
            for key, value in self.victories.items():
                file.write(f"{key},{value}\n")


    def get_fight_order(self, pokemon1: Pokemon, pokemon2: Pokemon):
        pokemon1_speed = (
            pokemon1.speed * stat_modifier_multiplier[pokemon1.n_speed_modifier]
        )
        pokemon2_speed = (
            pokemon2.speed * stat_modifier_multiplier[pokemon2.n_speed_modifier]
        )
        if pokemon1_speed > pokemon2_speed:
            self.attacks_first = self.team1
            self.attacks_second = self.team2
            return pokemon1, pokemon2
        elif pokemon1_speed < pokemon2_speed:
            self.attacks_first = self.team2
            self.attacks_second = self.team1
            return pokemon2, pokemon1
        else:
            if random.choice([True, False]):
                self.attacks_first = self.team1
                self.attacks_second = self.team2
                return pokemon1, pokemon2
            else:
                self.attacks_first = self.team2
                self.attacks_second = self.team1
                return pokemon2, pokemon1
