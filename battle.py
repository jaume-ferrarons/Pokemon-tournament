from models.movement import MovementKind, Movement
from models.pokemon import Pokemon, Team
import random
from logger import logger
from pokedex import Pokedex


class Battle:

    victories = {}
    attacks_first = None
    attacks_second = None

    stat_modifier_multiplier = {
        0: 1,
        1: 1.5,
        2: 2,
        3: 2.5,
        4: 3,
        5: 3.5,
        6: 4,
        -1: 2 / 3,
        -2: 1 / 2,
        -3: 0.4,
        -4: 1 / 3,
        -5: 2 / 7,
        -6: 1 / 4,
    }
    stat_modifier_map = {
        MovementKind.DECREASE_ATTACK: "n_attack_modifier",
        MovementKind.DECREASE_DEFENSE: "n_defense_modifier",
        MovementKind.DECREASE_SPECIAL_ATTACK: "n_sp_attack_modifier",
        MovementKind.DECREASE_SPECIAL_DEFENSE: "n_sp_defense_modifier",
        MovementKind.DECREASE_SPEED: "n_speed_modifier",
        MovementKind.INCREASE_ATTACK: "n_attack_modifier",
        MovementKind.INCREASE_DEFENSE: "n_defense_modifier",
        MovementKind.INCREASE_SPECIAL_ATTACK: "n_sp_attack_modifier",
        MovementKind.INCREASE_SPECIAL_DEFENSE: "n_sp_defense_modifier",
        MovementKind.INCREASE_SPEED: "n_speed_modifier",
        MovementKind.DECREASE_ACCURACY: "n_accuracy_modifier",
    }

    pokedex = Pokedex()

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
            t1_pokemon.stats["Total_turns"] += 1
            t2_pokemon.stats["Total_turns"] += 1
            first_attacker, second_attacker = self.get_fight_order(
                t1_pokemon, t2_pokemon
            )
            first_move = self.get_attack_move(
                first_attacker, self.attacks_first, second_attacker
            )
            attack_message = self.attack(first_move, first_attacker, second_attacker)
            logger.info(f"{self.battle_name}: {attack_message}")
            if second_attacker.is_alive():
                second_move = self.get_attack_move(
                    second_attacker, self.attacks_second, first_attacker
                )
                attack_message = self.attack(
                    second_move, second_attacker, first_attacker
                )
                logger.info(f"{self.battle_name}: {attack_message}")
            status = f"First attacker {first_attacker.name} has {first_attacker.hp} HP left, second attacker {second_attacker.name} has {second_attacker.hp} HP left"
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
        stats_file = f"{path}/fight_stats.csv"
        self.team1.save_stats(stats_file)
        self.team2.save_stats(stats_file)

    def get_fight_order(self, pokemon1: Pokemon, pokemon2: Pokemon):
        pokemon1_speed = (
            pokemon1.speed * self.stat_modifier_multiplier[pokemon1.n_speed_modifier]
        )
        pokemon2_speed = (
            pokemon2.speed * self.stat_modifier_multiplier[pokemon2.n_speed_modifier]
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

    def get_attack_move(
        self, attacker_pokemon: Pokemon, attacker_team: Team, defender_pokemon: Pokemon
    ):
        available_movements = attacker_pokemon.get_moves_with_pp()
        if available_movements:
            move = attacker_team.move_selector(attacker_pokemon.moves, attacker_team, defender_pokemon)
            move.consume_pp()
            attacker_pokemon.stats["Total_moves_used"] += 1
            return move
        else:
            logger.info("No PP left for this move! Using Struggle instead!")
            attacker_pokemon.stats["Count_struggle"] += 1
            return self.pokedex.movements["156"]

    # Will take a move, the attacking Pokemon object, and the defending Pokemon object as input
    # Will return a string that contains the amount of damage done and the effectiveness of the move
    def attack(self, move: Movement, attacker: Pokemon, defender: Pokemon):
        # Creating an empty string to store the results of the attack function
        attack_message = ""
        attack_message += attacker.name + " used " + move.name + "!" + "\n"

        # ATK/DEF or SpATK/SpDEF or Status? Using the Pokemon damage formula
        # If the move is "Physical", the damage formula will take into account attack and defense

        damage = 0
        logger.debug(
            f"Pokemon {attacker.name} used {move.name} of type {move.kind.name} against {defender.name}"
        )
        if move.id == "156":
            attack_message += "Attacker used Struggle!"
            damage, type_modifier = self.calculate_damage(move, attacker, defender)
            self_damage = damage / 2
            attacker.stats["Total_damage_done"] += damage
            logger.debug(
                f"Struggle case, defender {defender.name} HP before receiving damage: {defender.hp}, receiving {damage} damage"
            )
            logger.debug(
                f"Struggle case, attacker {attacker.name}HP before receiving damage: {attacker.hp}, receiving {self_damage} damage"
            )
            has_kill_defender = defender.receive_damage(damage)
            has_kill_attacker = attacker.receive_damage(self_damage)
            if has_kill_defender:
                attacker.stats["Total_kills"] += 1
            if has_kill_attacker:
                defender.stats["Total_kills"] += 1
            attack_message += f"\n{attacker.name} received recoil damage!"
            return attack_message

        # Going through each kind of different stat change based on the move type
        if move.kind in self.stat_modifier_map:
            if "DECREASE" in move.kind.name:
                attack_message = self.apply_stat_modifier(defender, move.kind)
                defender.stats["Total_debuffs_received"] += 1
            else:
                attack_message = self.apply_stat_modifier(attacker, move.kind)
                attacker.stats["Total_buffs_received"] += 1

        # Super effective, not very effective, or no effect?
        # Appending the result to tempMsg
        if move.kind in [MovementKind.PHYSICAL, MovementKind.SPECIAL]:
            logger.debug(f"Calculating damage for {move.name}")
            damage, type_modifier = self.calculate_damage(move, attacker, defender)
            if damage == 0:
                attack_message += "\n" + attacker.name + " missed!"
            elif 0.85 > type_modifier > 0:
                attack_message += "\nIt's not very effective..."
                attacker.stats["Total_not_effective"] += 1
            elif type_modifier > 1.5:
                attack_message += "\nIt's super effective!"
                attacker.stats["Total_super_effective"] += 1
            elif type_modifier == 0.0:
                attack_message += "\nIt doesn't affect " + defender.name + "..."
                attacker.stats["Total_no_effect"] += 1

        logger.debug(
            f"Defender {defender.name} HP before receiving damage: {defender.hp}, receiving {damage} damage"
        )
        is_kill = defender.receive_damage(damage)
        if is_kill:
            attacker.stats["Total_kills"] += 1
        is_one_shot = defender.is_one_shot(damage)
        if is_one_shot:
            attacker.stats["Total_one_shot"] += 1
        attacker.stats["Total_damage_done"] += damage

        # String containing useMove(), damage, and type effectiveness
        return attack_message

    def get_type_modifier(self, move: Movement, attacker: Pokemon, defender: Pokemon):
        # This modifier is used in damage calculations; it takes into account type advantage and STAB bonus
        modifier = 1
        modifier *= self.pokedex.get_multiplier(move.type, defender.type1)
        modifier *= self.pokedex.get_multiplier(move.type, defender.type2)
        if move.type in [attacker.type1, attacker.type2]:
            modifier *= Pokemon.SAME_TYPE_ATTACK_BONUS
        modifier *= random.uniform(0.85, 1.0)
        return modifier

    def calculate_damage(self, move: Movement, attacker: Pokemon, defender: Pokemon):
        type_modifier = self.get_type_modifier(move, attacker, defender)
        logger.debug(f"Type modifier: {type_modifier}")
        final_accuracy = (
            move.accuracy
            * 100
            * self.stat_modifier_multiplier[attacker.n_accuracy_modifier]
        )
        logger.debug(f"Final accuracy: {final_accuracy}")
        is_hit = random.randint(0, 100) < final_accuracy
        if not is_hit:
            attacker.stats["Total_misses"] += 1
            return 0, type_modifier
        if move.kind == MovementKind.PHYSICAL:
            attack = (
                attacker.attack
                * self.stat_modifier_multiplier[attacker.n_attack_modifier]
            )
            defense = (
                defender.defense
                * self.stat_modifier_multiplier[defender.n_defense_modifier]
            )
            kind_modifier = attack / defense
        elif move.kind == MovementKind.SPECIAL:
            sp_attack = (
                attacker.sp_attack
                * self.stat_modifier_multiplier[attacker.n_sp_attack_modifier]
            )
            sp_defense = (
                defender.sp_defense
                * self.stat_modifier_multiplier[defender.n_sp_defense_modifier]
            )
            kind_modifier = sp_attack / sp_defense
        else:
            # Status moves do not deal damage
            return 0
        level_modifier = (2 * attacker.LEVEL + 10) / 250
        logger.debug(
            f"Level modifier: {level_modifier}, Kind modifier: {kind_modifier}, Type modifier: {type_modifier}, Move power: {move.power}"
        )
        min_damage = 1
        damage = int(
            (level_modifier * kind_modifier * move.power + min_damage) * type_modifier
        )
        return damage, type_modifier

    def apply_stat_modifier(self, pokemon, kind):
        if kind in self.stat_modifier_map:
            attr = self.stat_modifier_map[kind]
            value = 1 if "INCREASE" in kind.name else -1
            if abs(getattr(pokemon, attr)) == 6:
                return f"{pokemon.name}'s {attr} maxed out!"
            setattr(pokemon, attr, getattr(pokemon, attr) + value)
            return f"{pokemon.name}'s applied {kind.name}!"
