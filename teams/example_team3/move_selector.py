from models.pokemon import Pokemon

def select_move(attacker: Pokemon, defender: Pokemon):
    max(attacker.moves, key=lambda x: x.power)
    return attacker.moves[0]