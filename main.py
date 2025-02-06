import os
import json
import random

from Game import CodeNamesGame
from Player import Player, ALLOWED_PLAYERS

def get_teams(red_team, blue_team):
    red_model, _ = red_team
    blue_model, _ = blue_team

    red_spymaster = Player("red", "spymaster", red_model)
    red_guesser = Player("red", "guesser", red_model)

    blue_spymaster = Player("blue", "spymaster", blue_model)
    blue_guesser = Player("blue", "guesser", blue_model)

    return red_spymaster, red_guesser, blue_spymaster, blue_guesser

def get_log_path(log_dir="logs"):
    os.makedirs(log_dir, exist_ok=True)
    game_numbers = [
        int(f[5:]) for f in os.listdir(log_dir) if f.startswith("game_") and f[5:].isdigit()
    ]
    next_number = max(game_numbers, default=0) + 1

    return os.path.join(log_dir, f"game_{next_number}")


if __name__ == "__main__":
    # TODO: get args
    args = None

    for simulation in range(args.num_simulations):
        red_team, blue_team = random.sample(ALLOWED_PLAYERS, 2)
        red_spymaster, red_guesser, blue_spymaster, blue_guesser = get_teams(
            red_team, blue_team
        )

        game = CodeNamesGame(
            red_spymaster=red_spymaster,
            red_guesser=red_guesser,
            blue_spymaster=blue_spymaster,
            blue_guesser=blue_guesser,
        )
        game.run()

        log_data = {
            "blue": blue_team[1],
            "red": red_team[1],
            "started": game.start_team,
            "winner": game.winner,
            "win_type": game.win_type,
            "words": game.game_words,
            "word_assignments": game.word_assignments,
            "turn_history": game.turn_history,
        }
        with open(get_log_path(args.log_dir), "w") as f:
            json.dump(log_data, f)