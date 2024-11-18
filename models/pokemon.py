from typing import List, Optional
from models.movement import Movement, MovementKind
from models.pokemon_type import PokemonType
import copy
import random


class Pokemon:

    # Values used to calculate Pokemon base stats
    IV = 30
    EV = 85
    SAME_TYPE_ATTACK_BONUS = 1.5  # Stands for "Same-type attack bonus"
    LEVEL = 50
    stats = {}

    def __init__(
        self,
        name: str,
        type1: PokemonType,
        type2: Optional[PokemonType],
        hp: int,
        attack: int,
        defense: int,
        sp_attack: int,
        sp_defense: int,
        speed: int,
        moves: List[Movement],
    ):
        self.name = name
        self.type1 = type1
        self.type2 = type2
        self.original_hp = hp
        self.original_attack = attack
        self.original_defense = defense
        self.original_sp_attack = sp_attack
        self.original_sp_defense = sp_defense
        self.original_speed = speed
        self.max_hp = hp + Pokemon.IV * 0.5 + Pokemon.EV * 0.125 + 60
        self.hp = self.max_hp
        self.attack = attack + Pokemon.IV * 0.5 + Pokemon.EV * 0.125 + 5
        self.defense = defense + Pokemon.IV * 0.5 + Pokemon.EV * 0.125 + 5
        self.sp_attack = sp_attack + Pokemon.IV * 0.5 + Pokemon.EV * 0.125 + 5
        self.sp_defense = sp_defense + Pokemon.IV * 0.5 + Pokemon.EV * 0.125 + 5
        self.speed = speed + Pokemon.IV * 0.5 + Pokemon.EV * 0.125 + 5
        self.n_attack_modifier = 0
        self.n_defense_modifier = 0
        self.n_sp_attack_modifier = 0
        self.n_sp_defense_modifier = 0
        self.n_speed_modifier = 0
        self.n_accuracy_modifier = 0
        self.moves = moves
        self.stats = {
            "Count_struggle": 0,
            "Total_moves_used": 0,
            "Total_damage_done": 0,
            "Total_damage_received": 0,
            "Total_kills": 0,
            "Total_buffs_received": 0,
            "Total_debuffs_received": 0,
            "Total_misses": 0,
            "Total_not_effective": 0,
            "Total_super_effective": 0,
            "Total_one_shot": 0,
            "Total_no_effect": 0,
            "Total_turns": 0,
        }

    def __copy__(self):
        return Pokemon(
            self.name,
            self.type1,
            self.type2,
            self.original_hp,
            self.original_attack,
            self.original_defense,
            self.original_sp_attack,
            self.original_sp_defense,
            self.original_speed,
            [copy.copy(move) for move in self.moves],
        )

    def receive_damage(self, damage: int) -> bool:
        self.hp = self.hp - damage
        self.stats["Total_damage_received"] += damage
        if self.hp < 0:
            self.hp = 0
            is_kill = True
        else:
            is_kill = False
        return is_kill

    def is_alive(self):
        return self.hp > 0

    def get_moves_with_pp(self):
        return [move for move in self.moves if move.pp > 0]

    def is_one_shot(self, damage: int) -> bool:
        return damage >= self.max_hp

    def heal(self):
        self.hp = self.max_hp
        self.n_attack_modifier = 0
        self.n_defense_modifier = 0
        self.n_sp_attack_modifier = 0
        self.n_sp_defense_modifier = 0
        self.n_speed_modifier = 0
        self.n_accuracy_modifier = 0
        for move in self.moves:
            move.reset_pp()


def select_move(attacker_moves: List[Movement], attacker:Pokemon, defender: Pokemon):
    return random.choice(attacker_moves)


class Team:

    def __init__(self, pokemons: List[Pokemon], name: str):
        self.pokemons = pokemons
        self.name = name
        self.move_selector = select_move

    def is_defeated(self):
        return all(not pokemon.is_alive() for pokemon in self.pokemons)

    def get_pokemon(self):
        for pokemon in self.pokemons:
            if pokemon.is_alive():
                return pokemon

    def count_alive_pokemons(self):
        return sum(pokemon.is_alive() for pokemon in self.pokemons)

    def set_select_move(self, move_selector: callable):
        self.move_selector = move_selector

    def reset_team(self):
        for pokemon in self.pokemons:
            pokemon.heal()

    def save_stats(self, path_to_save):
        with open(path_to_save, mode="a", newline="") as file:
            for pokemon in self.pokemons:
                for key, value in pokemon.stats.items():
                    file.write(f"{self.name},{pokemon.name},{key},{value}\n")

    def is_valid_team(self):
        has_right_number_of_pokemons = len(self.pokemons) == 6
        has_right_number_of_movements = all(
            len(pokemon.moves) == 4 for pokemon in self.pokemons
        )
        has_valid_movements = all(
            move.id != "156" for pokemon in self.pokemons for move in pokemon.moves
        )
        has_valid_move_selector = self.check_move_selector()
        return all(
            [
                has_right_number_of_pokemons,
                has_right_number_of_movements,
                has_valid_move_selector,
                has_valid_movements,
            ]
        )

    def check_move_selector(self) -> bool:
        pokemon1_movements = [
            Movement(
                "1",
                "dummy1",
                "dummy",
                PokemonType.NORMAL,
                MovementKind.PHYSICAL,
                100,
                "100%",
                100,
            ),
            Movement(
                "2",
                "dummy2",
                "dummy",
                PokemonType.NORMAL,
                MovementKind.PHYSICAL,
                100,
                "100%",
                100,
            ),
            Movement(
                "3",
                "dummy3",
                "dummy",
                PokemonType.NORMAL,
                MovementKind.PHYSICAL,
                100,
                "100%",
                100,
            ),
            Movement(
                "4",
                "dummy4",
                "dummy",
                PokemonType.NORMAL,
                MovementKind.PHYSICAL,
                100,
                "100%",
                100,
            ),
        ]
        pokemon2_movements = [
            Movement(
                "5",
                "dummy5",
                "dummy",
                PokemonType.NORMAL,
                MovementKind.PHYSICAL,
                100,
                "100%",
                100,
            ),
            Movement(
                "6",
                "dummy6",
                "dummy",
                PokemonType.NORMAL,
                MovementKind.PHYSICAL,
                100,
                "100%",
                100,
            ),
            Movement(
                "7",
                "dummy7",
                "dummy",
                PokemonType.NORMAL,
                MovementKind.PHYSICAL,
                100,
                "100%",
                100,
            ),
            Movement(
                "8",
                "dummy8",
                "dummy",
                PokemonType.NORMAL,
                MovementKind.PHYSICAL,
                100,
                "100%",
                100,
            ),
        ]
        dummy_pokemon1 = Pokemon(
            "dummy",
            PokemonType.NORMAL,
            None,
            100,
            100,
            100,
            100,
            100,
            100,
            pokemon1_movements,
        )
        dummy_pokemon2 = Pokemon(
            "dummy2",
            PokemonType.NORMAL,
            None,
            100,
            100,
            100,
            100,
            100,
            100,
            pokemon2_movements,
        )
        movement = self.move_selector(dummy_pokemon1.moves,dummy_pokemon1, dummy_pokemon2)
        return movement in pokemon1_movements
