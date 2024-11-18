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
        id: str,
        name: str,
        effect: str,
        type: PokemonType,
        kind: MovementKind,
        power: int,
        accuracy: Optional[float],
        pp: int,
    ):
        self.id = id
        self.name = name
        self.effect = effect
        self.type = type
        self.kind = kind
        self.power = power
        self.accuracy = accuracy
        self.pp = pp
        self.max_pp = pp

    def consume_pp(self):
        if self.pp > 0:
            self.pp -= 1

    def reset_pp(self):
        self.pp = self.max_pp

    def __copy__(self):
        return Movement(
            self.id,
            self.name,
            self.effect,
            self.type,
            self.kind,
            self.power,
            self.accuracy,
            self.max_pp,
        )
