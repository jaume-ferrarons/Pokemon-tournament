from typing import List
from models.pokemon import Pokemon
from models.movement import Movement

def select_move(attacker_moves: List[Movement], attacker:Pokemon, defender: Pokemon):
    return attacker_moves[0]