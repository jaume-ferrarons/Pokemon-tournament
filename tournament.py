# This is a sample Python script.
from pokedex import Pokedex
from models.pokemon import Team
from battle import Battle
from typing import List
from logger import logger
import os
from importlib import util
import copy

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

pokedex = Pokedex()


def load_team(team_file, team_name=None) -> Team:
    print(team_file)
    pokemons = []
    with open(team_file) as f:
        lines = f.readlines()
        for line in lines[1:]:
            pokemon_id, *moves = line.strip().split(",")
            pokemon = copy.copy(pokedex.pokemon[pokemon_id.strip()])
            pokemon.moves = [copy.copy(pokedex.movements[move_id.strip()]) for move_id in moves]
            pokemons.append(pokemon)
    team = Team(pokemons, team_name)
    team_dir_name = os.path.dirname(team_file)
    for file in [f for f in os.listdir(team_dir_name) if ".py" in f]:
        module_path = os.path.join(team_dir_name, file)
        spec = util.spec_from_file_location(team_name + "-selector", module_path)
        module = util.module_from_spec(spec)
        spec.loader.exec_module(module)
        select_move = getattr(module, "select_move", team.move_selector)
        team.set_select_move(select_move)
    if not team.is_valid_team():
        raise ValueError(f"Invalid team: {team_name}")
    return team


def get_teams() -> List[Team]:
    """Get available teams from the teams folder and load them"""
    teams = []
    for root, dirs, files in os.walk("./teams"):
        for file in files:
            if ".csv" in file:
                team_path = os.path.join(root, file)
                team_name = team_path.split("/teams")[1].split("/")[1]
                team = load_team(team_path, team_name)
                teams.append(team)
    return teams


def get_encounter_combinations(teams: List[Team]):
    import itertools

    return list(itertools.combinations(teams, 2))


def compute_lead_board():
    results = {}
    for file in os.listdir("./results"):
        if "stats" not in file:
            with open(f"./results/{file}") as f:
                lines = f.readlines()
                for line in lines:
                    team, victories = line.strip().split(",")
                    if team not in results:
                        results[team] = 0
                    results[team] += int(victories)
    sorted_results = dict(
        sorted(results.items(), key=lambda item: item[1], reverse=True)
    )
    with open("./results/lead_board.txt", mode="w", newline="") as file:
        for index, key_value_tuple in enumerate(sorted_results.items()):
            key, value = key_value_tuple
            file.write(f"|{index+1}|{key}|{value}|\n")
    return sorted_results

def clean_files():
    if os.path.exists("./results"):
        for file in os.listdir("./results"):
            os.remove(f"./results/{file}")


# Press the green button in the gutter to run the script.
if __name__ == "__main__":
    teams = get_teams()
    combinations = get_encounter_combinations(teams)
    battles = [Battle(team1, team2) for team1, team2 in combinations]
    clean_files()
    for battler in battles:
        logger.info(
            f"Starting battle between {battler.team1.name} and {battler.team2.name}"
        )
    results_path = "./results"
    if not os.path.exists(results_path):
        os.makedirs(results_path)
    for battle in battles:
        battle.best_of_n(n=5)
        logger.info(f"Results: {battle.victories}")
        battle.save_results("./results")
    logger.info(f"Lead board: {compute_lead_board()}")

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
