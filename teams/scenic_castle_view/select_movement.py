import random


def select_move(attacker_moves, attacker, defender):
    order = [236, 237, 145, 114]

    for id_ in order:
        if id_ in [m.id for m in attacker_moves]:
            return [m for m in attacker_moves if m.id == id_][0]
    else:
        return random.choice(attacker_moves)
