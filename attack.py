from models.movement import Movement, MovementKind
from models.pokemon import Pokemon
from pokedex import Pokedex
import random
from logger import logger


stat_modifier_multiplier = {
    0: 1,
    1: 1.5,
    2: 2,
    3: 2.5,
    4: 3,
    5: 3.5,
    6: 4,
    -1: 2 / 3,
    -2: 1 / 2,
    -3: 0.4,
    -4: 1 / 3,
    -5: 2 / 7,
    -6: 1 / 4,
}
stat_modifier_map = {
    MovementKind.DECREASE_ATTACK: "n_attack_modifier",
    MovementKind.DECREASE_DEFENSE: "n_defense_modifier",
    MovementKind.DECREASE_SPECIAL_ATTACK: "n_sp_attack_modifier",
    MovementKind.DECREASE_SPECIAL_DEFENSE: "n_sp_defense_modifier",
    MovementKind.DECREASE_SPEED: "n_speed_modifier",
    MovementKind.INCREASE_ATTACK: "n_attack_modifier",
    MovementKind.INCREASE_DEFENSE: "n_defense_modifier",
    MovementKind.INCREASE_SPECIAL_ATTACK: "n_sp_attack_modifier",
    MovementKind.INCREASE_SPECIAL_DEFENSE: "n_sp_defense_modifier",
    MovementKind.INCREASE_SPEED: "n_speed_modifier",
    MovementKind.DECREASE_ACCURACY: "n_accuracy_modifier",
}

pokedex = Pokedex()


# Will take a move, the attacking Pokemon object, and the defending Pokemon object as input
# Will return a string that contains the amount of damage done and the effectiveness of the move
def attack(move: Movement, attacker: Pokemon, defender: Pokemon):
    # Creating an empty string to store the results of the attack function
    attack_message = ""
    attack_message += attacker.name + " used " + move.name + "!" + "\n"

    # ATK/DEF or SpATK/SpDEF or Status? Using the Pokemon damage formula
    # If the move is "Physical", the damage formula will take into account attack and defense

    damage = 0
    logger.debug(f"Move kind: {move.kind.name}")
    # Going through each kind of different stat change based on the move type
    if move.kind in stat_modifier_map:
        logger.debug(f"Modifying pokemon stats")
        if "DECREASE" in move.kind.name:
            attack_message = apply_stat_modifier(defender, move.kind)
        else:
            attack_message = apply_stat_modifier(attacker, move.kind)

    # Super effective, not very effective, or no effect?
    # Appending the result to tempMsg
    if move.kind in [MovementKind.PHYSICAL, MovementKind.SPECIAL]:
        logger.debug(f"Calculating damage for {move.name}")
        damage, type_modifier = calculate_damage(move, attacker, defender)
        if damage == 0:
            attack_message += "\n" + attacker.name + " missed!"
        elif 0.85 > type_modifier > 0:
            attack_message += "\nIt's not very effective..."
        elif type_modifier > 1.5:
            attack_message += "\nIt's super effective!"
        elif type_modifier == 0.0:
            attack_message += "\nIt doesn't affect " + defender.name + "..."

    logger.debug(f"Defender HP before receiving damage: {defender.hp}")
    logger.debug(f"Damage: {damage}")
    defender.receive_damage(damage)
    logger.debug(f"Defender HP after receiving damage: {defender.hp}")

    # String containing useMove(), damage, and type effectiveness
    return attack_message


def get_type_modifier(move: Movement, attacker: Pokemon, defender: Pokemon):
    # This modifier is used in damage calculations; it takes into account type advantage and STAB bonus
    modifier = 1
    modifier *= pokedex.get_multiplier(move.type, defender.type1)
    modifier *= pokedex.get_multiplier(move.type, defender.type2)
    if move.type in [attacker.type1, attacker.type2]:
        modifier *= Pokemon.SAME_TYPE_ATTACK_BONUS
    modifier *= random.uniform(0.85, 1.0)
    return modifier


def calculate_damage(move: Movement, attacker: Pokemon, defender: Pokemon):
    type_modifier = get_type_modifier(move, attacker, defender)
    final_accuracy = (
            move.accuracy * 100 * stat_modifier_multiplier[attacker.n_accuracy_modifier]
    )
    logger.debug(f"Final accuracy: {final_accuracy}")
    is_hit = random.randint(0, 100) < final_accuracy
    min_damage = 1
    if not is_hit:
        return min_damage, type_modifier
    if move.kind == MovementKind.PHYSICAL:
        attack = attacker.attack * stat_modifier_multiplier[attacker.n_attack_modifier]
        defense = (
                defender.defense * stat_modifier_multiplier[defender.n_defense_modifier]
        )
        kind_modifier = attack / defense
    elif move.kind == MovementKind.SPECIAL:
        sp_attack = (
                attacker.sp_attack * stat_modifier_multiplier[attacker.n_sp_attack_modifier]
        )
        sp_defense = (
                defender.sp_defense
                * stat_modifier_multiplier[defender.n_sp_defense_modifier]
        )
        kind_modifier = sp_attack / sp_defense
    else:
        # Status moves do not deal damage
        return 0
    level_modifier = (2 * attacker.LEVEL + 10) / 250
    logger.debug(
        f"Level modifier: {level_modifier}, \nKind modifier: {kind_modifier}, \nType modifier: {type_modifier}, \nMove power: {move.power}"
    )
    damage = int(
        (level_modifier * kind_modifier * move.power + min_damage) * type_modifier
    )
    return damage, type_modifier


def apply_stat_modifier(pokemon, kind):
    if kind in stat_modifier_map:
        attr = stat_modifier_map[kind]
        value = 1 if "INCREASE" in kind.name else -1
        if abs(getattr(pokemon, attr)) == 6:
            return f"{pokemon.name}'s {attr} maxed out!"
        setattr(pokemon, attr, getattr(pokemon, attr) + value)
        return f"{pokemon.name}'s applied {kind.name}!"
