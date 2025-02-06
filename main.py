import os
import json
import random
import argparse

from Game import CodeNamesGame
from Player import Player, ALLOWED_PLAYERS

def get_teams(red_team, blue_team):
    red_spymaster = Player("red", "spymaster", red_team)
    red_guesser = Player("red", "guesser", red_team)

    blue_spymaster = Player("blue", "spymaster", blue_team)
    blue_guesser = Player("blue", "guesser", blue_team)

    return red_spymaster, red_guesser, blue_spymaster, blue_guesser

def get_log_path(log_dir="logs/"):
    os.makedirs(log_dir, exist_ok=True)
    game_numbers = [
        int(f[5:]) for f in os.listdir(log_dir) if f.startswith("game_") and f[5:].isdigit()
    ]
    next_number = max(game_numbers, default=0) + 1

    return os.path.join(log_dir, f"game_{next_number}")

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--num_simulations",
        type=int,
        default=10,
        help="Number of simulations to run.",
    )
    parser.add_argument(
        "--log_dir", type=str, default="logs/", help="Directory to save game logs."
    )

    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()

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
