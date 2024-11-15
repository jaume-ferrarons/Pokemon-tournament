from typing import Optional
from models.pokemon import Pokemon
from models.movement import Movement, MovementKind
from models.pokemon_type import PokemonType
from logger import logger


class Pokedex:
    """
    This class loads the pokemons from the data/pokemon.csv file and stores them in a dictionary by their id.
    """

    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(Pokedex, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        if not hasattr(self, 'initialized'):  # Ensure the initialization code runs only once
            self.pokemon = {}
            self.movements = {}
            self.type_advantages = {}
            self.load_pokemon()
            self.load_movements()
            self.load_type_advantages()
            self.initialized = True

    def load_pokemon(self):
        with open("./data/pokemons.csv") as f:
            lines = f.readlines()
            for line in lines[1:]:
                (
                    id,
                    name,
                    type1,
                    type2,
                    hp,
                    attack,
                    defense,
                    sp_attack,
                    sp_defense,
                    speed,
                ) = line.strip().split(",")
                self.pokemon[id] = Pokemon(
                    name,
                    PokemonType(type1),
                    PokemonType(type2) if type2 != "" else None,
                    int(hp),
                    int(attack),
                    int(defense),
                    int(sp_attack),
                    int(sp_defense),
                    int(speed),
                    [],
                )

    def load_movements(self):
        with open("./data/movements.csv") as f:
            lines = f.readlines()
            for line in lines[1:]:
                id, name, effect, type, kind, power, accuracy, pp = line.strip().split(
                    ","
                )
                self.movements[id] = Movement(
                    name,
                    effect,
                    PokemonType(type),
                    MovementKind(kind),
                    int(power),
                    accuracy,
                    pp,
                )

    def load_type_advantages(self):
        with open("./data/type_advantages.csv") as f:
            lines = f.readlines()
            for line in lines[1:]:
                key, attack_type, defense_type, multiplier = line.strip().split(",")
                pair_attack_defense = (
                    PokemonType(attack_type),
                    PokemonType(defense_type),
                )
                self.type_advantages[pair_attack_defense] = float(multiplier)

    def get_multiplier(
        self, attack_type: PokemonType, defense_type: Optional[PokemonType]
    ):
        logger.debug(f"Getting multiplier for {attack_type} and {defense_type}")
        if defense_type is None:
            return 1.0
        return self.type_advantages.get((attack_type, defense_type), 1.0)
