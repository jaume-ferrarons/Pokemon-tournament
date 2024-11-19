from typing import List
from models.movement import Movement
from models.pokemon import Pokemon


def select_move(attacker_moves: List[Movement], attacker: Pokemon, defender: Pokemon):
    move = max(attacker_moves, key=lambda x: x.power)
    return move
