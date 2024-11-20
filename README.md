# Altafulla code challenge - Pokemon tournament
![](https://github.com/hectormirete/Pokemon-tournament/actions/workflows/tournament.yml/badge.svg)
## Leaderboard
| Rank | Team | Score |
| --- | --- | --- |
|1|scenic_castle_view|30|
|2|ash-ketchum|29|
|3|not-so-smart|23|
|4|RegressionRangers|22|
|5|cloud_migration|19|
|6|KoF|11|
|7|martini|6|
|8|ev3n-w0rse-than-mats|0|

## How to contribute
* Clone the repository
* Create a new branch
* Create your team:
  * Create a new folder under [teams](./teams) with your team name. the folder will be your team name
    * Add there a `.csv` file with your team and the pokemon movements
      * The file must contain on each row the pokemon id and the movement id separated by a comma
      * Each pokemon must have 4 movements
      * Each team must have 6 pokemons
        * Example:
          ```
          Pokemon, move1, move2, move3, move4
          23,23,34,65,54
          12,150,263,45,74
          149,70,92,259,93
          93,79,265,43,263
          54,47,74,55,97
          8,17,42,4,96
          ```
    * You can end here. If you do, the movement that your pokemon will use will be random
    * If you want to specify the movement that your pokemon will use, you can create a `.py` file with a function that selects
      the movement to use. 
      * This function must be named `select_movement` and receive a list of attacker_movements and the pokemon defender.
        * Example:
          ```python
          def select_move(attacker_moves: List[Movement], attacker:Pokemon, defender: Pokemon):
            return random.choice(attacker_moves)
          ```
        
## How to run the project
You can run the tournament locally to see how your team performs
```
export PYTHONPATH=$(pwd):$PYTHONPATH
python tournament.py
```
Note: There is not need of using poetry to run the project, but if you want to use it, you can install the dependencies with
```
poetry install
## And then
export PYTHONPATH=$(pwd):$PYTHONPATH
poetry run python tournament.py
```
Have fun :) 