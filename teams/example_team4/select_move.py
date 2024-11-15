from models.pokemon import Pokemon

def select_move(attacker: Pokemon, defender: Pokemon):
    return attacker.moves[0]