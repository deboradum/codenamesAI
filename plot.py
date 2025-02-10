import os
import json

import numpy as np
import matplotlib.pyplot as plt

from matplotlib.ticker import MaxNLocator


def plot_average_spymaster_num_cards(data, save_path):
    spymaster_counts = {}

    # Iterate over games to collect spymaster numbers
    for game in data:
        blue_team = game["blue"]
        red_team = game["red"]

        if blue_team not in spymaster_counts:
            spymaster_counts[blue_team] = []
        if red_team not in spymaster_counts:
            spymaster_counts[red_team] = []

        # Extract spymaster numbers from turn history
        for turn in game["turn_history"]:
            team = game[turn["team"]]  # Get team name
            num_cards = int(turn["spymaster"][1])  # Second element is the number given

            spymaster_counts[team].append(num_cards)

    # Compute averages
    teams = list(spymaster_counts.keys())
    avg_cards = [np.mean(spymaster_counts[team]) for team in teams]

    # Plot results
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(
        teams,
        avg_cards,
    )

    # Labels and title
    ax.set_ylabel("Average Number Given by Spymaster")
    ax.set_title("Average Spymaster Numbers per Team")

    # Ensure y-axis shows only whole numbers
    ax.yaxis.set_major_locator(plt.MaxNLocator(integer=True))

    # Rotate x-axis labels for readability
    plt.xticks(rotation=45, ha="right")

    # Save plot
    plt.tight_layout()
    plt.savefig(save_path)


def plot_win_rates(data, save_path):
    win_data = {}
    games_played = {}

    # Count wins by team, win type, and games played
    for game in data:
        blue_team = game["blue"]
        red_team = game["red"]
        winner = game[game["winner"]]  # Get the winning team
        win_type = game["win_type"]  # Get the win type

        # For blue team
        if blue_team not in win_data:
            win_data[blue_team] = {
                "total_wins": 0,
                "win_types": {"correct_guess": 0, "incorrect_guess": 0, "assassin": 0},
            }
            games_played[blue_team] = 0  # Track games played by blue team
        # For red team
        if red_team not in win_data:
            win_data[red_team] = {
                "total_wins": 0,
                "win_types": {"correct_guess": 0, "incorrect_guess": 0, "assassin": 0},
            }
            games_played[red_team] = 0  # Track games played by red team

        # Increment total games played for each team
        games_played[blue_team] += 1
        games_played[red_team] += 1

        # Increment win type count for the winning team
        win_data[winner]["total_wins"] += 1
        win_data[winner]["win_types"][win_type] += 1

    # Prepare data for the plot
    teams = list(win_data.keys())
    total_wins = [win_data[team]["total_wins"] for team in teams]
    total_games = [games_played[team] for team in teams]
    win_types = [win_data[team]["win_types"] for team in teams]

    # Set up colors for different win types
    win_type_colors = {
        "correct_guess": "blue",
        "incorrect_guess": "red",
        "assassin": "green",
    }

    fig, ax = plt.subplots(figsize=(10, 6))

    # Create stacked bars for each team
    bar_bottom = [0] * len(teams)  # To stack the win types
    for win_type, color in win_type_colors.items():
        win_type_counts = [
            win_data[team]["win_types"].get(win_type, 0) for team in teams
        ]
        ax.bar(teams, win_type_counts, bottom=bar_bottom, color=color, label=win_type)

        # Update the bottom for the next stack
        bar_bottom = [bar_bottom[i] + win_type_counts[i] for i in range(len(teams))]

    # Add labels and title
    ax.set_ylabel("Number of Wins")
    ax.set_title(f"Team Win Counts by Win Type ({len(data)} games)")
    ax.legend(title="Win Types", loc="upper right", bbox_to_anchor=(1.05, 1))
    # Calculate and display win rates above the bars
    for i, team in enumerate(teams):
        win_rate = (
            total_wins[i] / total_games[i] * 100
        )  # Calculate win rate as a percentage
        ax.text(
            teams[i], total_wins[i] + 0.5, f"{win_rate:.2f}%", ha="center", va="bottom"
        )

    # Rotate the x-axis labels for better readability
    plt.xticks(rotation=45, ha="right")
    ax.yaxis.set_major_locator(MaxNLocator(integer=True))

    # Save the plot to the specified path
    plt.tight_layout()
    plt.savefig(save_path)


def plot_game_ending_types(data, save_path):
    # Initialize a dictionary to count occurrences of each win type
    win_type_counts = {"correct_guess": 0, "incorrect_guess": 0, "assassin": 0}

    # Count the occurrences of each win type
    for game in data:
        win_type = game["win_type"]
        if win_type in win_type_counts:
            win_type_counts[win_type] += 1

    # Data for the pie chart
    labels = list(win_type_counts.keys())
    sizes = list(win_type_counts.values())
    colors = ["blue", "red", "green"]  # Assign colors to each win type

    # Plot the pie chart
    fig, ax = plt.subplots(figsize=(7, 7))
    ax.pie(
        sizes,
        labels=labels,
        autopct="%1.1f%%",
        startangle=90,
        colors=colors,
        wedgeprops={"edgecolor": "black"},
    )
    ax.axis("equal")  # Equal aspect ratio ensures that pie is drawn as a circle

    # Add title
    ax.set_title(f"Distribution of Game Ending Types ({len(data)} games)")

    # Save the plot to the specified path
    plt.tight_layout()
    plt.savefig(save_path)


def plot_num_games_played(data, save_path):
    games_played = {}
    for game in data:
        blue_team = game["blue"]
        red_team = game["red"]
        if not games_played.get(blue_team):
            games_played[blue_team] = {"blue": 0, "red": 0}
        if not games_played.get(red_team):
            games_played[red_team] = {"blue": 0, "red": 0}
        games_played[blue_team]["blue"] += 1
        games_played[red_team]["red"] += 1

    teams = list(games_played.keys())
    blue_games = [games_played[team]["blue"] for team in teams]
    red_games = [games_played[team]["red"] for team in teams]

    # Create a bar plot
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(teams, blue_games, color="blue", label="Blue Team")
    ax.bar(teams, red_games, bottom=blue_games, color="red", label="Red Team")

    # Add labels and title
    ax.set_ylabel("Number of Games Played")
    ax.set_title(f"Games Played as Blue and Red Teams ({len(data)} games)")
    ax.legend()

    # Rotate the x-axis labels for better readability
    plt.xticks(rotation=45, ha="right")

    plt.tight_layout()
    plt.savefig(save_path)


def read_data(log_dir="logs/"):
    data = []
    for file_path in os.listdir(log_dir):
        if not file_path.endswith(".json"):
            continue
        with open(f"{log_dir}/{file_path}", "r") as f:
            data.append(json.load(f))

    return data


def plot_average_turns_per_game(data, save_path):
    turn_counts = {}

    for game in data:
        blue_team = game["blue"]
        red_team = game["red"]
        num_turns = len(game["turn_history"])

        if blue_team not in turn_counts:
            turn_counts[blue_team] = []
        if red_team not in turn_counts:
            turn_counts[red_team] = []

        turn_counts[blue_team].append(num_turns)
        turn_counts[red_team].append(num_turns)

    teams = list(turn_counts.keys())
    avg_turns = [np.mean(turn_counts[team]) for team in teams]

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(teams, avg_turns, color="purple")
    ax.set_ylabel("Average Turns per Game")
    ax.set_title(f"Average Turns per Game per Team ({len(data)} games)")
    ax.yaxis.set_major_locator(plt.MaxNLocator(integer=True))
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig(save_path)


def plot_guessing_accuracy_per_team(data, save_path):
    accuracy = {}

    for game in data:
        blue_team = game["blue"]
        red_team = game["red"]

        if blue_team not in accuracy:
            accuracy[blue_team] = {"correct": 0, "total": 0}
        if red_team not in accuracy:
            accuracy[red_team] = {"correct": 0, "total": 0}

        for turn in game["turn_history"]:
            team = game[turn["team"]]
            guesses = turn["guesser"]
            correct_guesses = sum(
                1 for word in guesses if word in game["word_assignments"][turn["team"]]
            )

            accuracy[team]["correct"] += correct_guesses
            accuracy[team]["total"] += len(guesses)

    teams = list(accuracy.keys())
    accuracy_rates = [
        accuracy[team]["correct"] / accuracy[team]["total"]
        if accuracy[team]["total"] > 0
        else 0
        for team in teams
    ]

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(teams, accuracy_rates, color="green")
    ax.set_ylabel("Guessing Accuracy")
    ax.set_title(f"Guessing Accuracy per Team ({len(data)} games)")
    ax.set_ylim(0, 1)
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig(save_path)


def plot_first_move_advantage(data, save_path):
    first_move_wins = {"started": 0, "not_started": 0}

    for game in data:
        if game["started"] == game["winner"]:
            first_move_wins["started"] += 1
        else:
            first_move_wins["not_started"] += 1

    fig, ax = plt.subplots(figsize=(8, 6))
    ax.bar(first_move_wins.keys(), first_move_wins.values(), color=["blue", "red"])
    ax.set_ylabel("Number of Wins")
    ax.set_title(f"First Move Advantage: Win Rate Comparison ({len(data)} games)")
    plt.tight_layout()
    plt.savefig(save_path)


if __name__ == "__main__":
    output_dir = "plots/"
    os.makedirs(output_dir, exist_ok=True)
    data = read_data(log_dir="logs/")

    plot_num_games_played(data, f"{output_dir}/num_games_played.png")
    plot_win_rates(data, f"{output_dir}/win_rates.png")
    plot_game_ending_types(data, f"{output_dir}/game_endings.png")
    plot_average_spymaster_num_cards(data, f"{output_dir}/avg_spymaster_card.png")
    plot_average_turns_per_game(data, f"{output_dir}/average_turns_per_game.png")
    plot_guessing_accuracy_per_team(
        data, f"{output_dir}/guessing_accuracy_per_team.png"
    )
    plot_first_move_advantage(data, f"{output_dir}/first_move_advantage.png")
