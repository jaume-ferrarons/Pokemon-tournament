from models.pokemon import Pokemon
from models.movement import Movement
from typing import List


def select_move(attacker_moves: List[Movement], attacker:Pokemon, defender: Pokemon):
    return attacker_moves[0]
