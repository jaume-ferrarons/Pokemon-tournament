def select_move(attacker_moves, attacker, defender):
    return max(attacker_moves, key=lambda move: move.power)
