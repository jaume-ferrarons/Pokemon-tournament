from models.pokemon_type import PokemonType
from typing import Optional
from enum import Enum


class MovementKind(Enum):
    PHYSICAL = "Physical"
    SPECIAL = "Special"
    INCREASE_ATTACK = "a+"
    DECREASE_ATTACK = "a-"
    INCREASE_DEFENSE = "d+"
    DECREASE_DEFENSE = "d-"
    INCREASE_SPECIAL_ATTACK = "sa+"
    DECREASE_SPECIAL_ATTACK = "sa-"
    INCREASE_SPECIAL_DEFENSE = "sd+"
    DECREASE_SPECIAL_DEFENSE = "sd-"
    INCREASE_SPEED = "s+"
    DECREASE_SPEED = "s-"
    DECREASE_ACCURACY = "acc-"


class Movement:

    def __init__(
        self,
        name: str,
        effect: str,
        type: PokemonType,
        kind: MovementKind,
        power: int,
        accuracy: Optional[str],
        pp: int,
    ):
        self.name = name
        self.effect = effect
        self.type = type
        self.kind = kind
        self.power = power
        if accuracy:
            acc = int(accuracy.split("%")[0])
            self.accuracy = float(acc / 100)
        else:
            self.accuracy = None
        self.pp = pp
