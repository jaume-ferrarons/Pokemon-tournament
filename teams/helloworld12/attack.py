import random
import pandas as pd
import copy

from models.pokemon import Pokemon, Team
from models.movement import Movement
from battle import Battle

def select_move(attacker_moves: list[Movement], attacker: Pokemon, defender: Pokemon, num_simulations: int = 10):
    """
    Select the best move using a Monte Carlo Tree Search-like approach.
    """
    # return random.choice(attacker_moves)
    best_move = None
    highest_score = -float("inf")

    move_scores = {move: 0 for move in attacker_moves}

    # Simulate each move's outcomes
    for move in attacker_moves:
        total_score = 0

        for _ in range(num_simulations):
            # Simulate the battle for this move
            score = simulate_battle_outcome(move, attacker, defender)
            total_score += score

        # Average score across simulations
        move_scores[move] = total_score / num_simulations

        # Track the best move
        if move_scores[move] > highest_score:
            highest_score = move_scores[move]
            best_move = move

    return best_move

class BattleWrapper:
    @staticmethod
    def get_type_modifier(move: Movement, attacker: Pokemon, defender: Pokemon):
        return Battle.get_type_modifier(Battle, move, attacker, defender)
    
    stat_modifier_multiplier =  Battle.stat_modifier_multiplier


def simulate_battle_outcome(move: Movement, attacker: Pokemon, defender: Pokemon):
    """
    Simulate the outcome of a battle turn using the given move.
    """
    if isinstance(move.accuracy, str) or move.accuracy is None:
        move = copy.deepcopy(move)
        if move.accuracy is None:
            move.accuracy = 1
        else:
            move.accuracy = float(move.accuracy.strip("%")) / 100

    # Calculate initial damage
    damage = Battle.calculate_damage(BattleWrapper, move, attacker, defender)
    if isinstance(damage, tuple):
        damage, type_modifier = damage

    # Evaluate the result
    if damage == 0:
        return -1  # Penalize misses
    elif type_modifier > 1.5:
        return damage + 5  # Reward super-effective moves
    elif type_modifier < 0.85:
        return damage - 5  # Penalize not-very-effective moves

    # Include additional rewards for KO or stat effects
    if defender.hp - damage <= 0:
        return 50  # High reward for a KO

    return damage  # Default reward is the damage dealt