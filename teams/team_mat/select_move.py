from models.pokemon import Pokemon
from models.movement import Movement
from typing import List

def select_move(attacker_moves: List[Movement], attacker:Pokemon, defender: Pokemon):
    move = min(attacker_moves, key=lambda x: x.power)
    return move
