import random

def get_random_words(wordlist_path="assets/words.txt", num_words=25):
    with open(wordlist_path, "r", encoding="utf-8") as file:
        words = file.read().splitlines()

    return random.sample(words, min(num_words, len(words)))


class CodeNamesGame:
    def __init__(self, red_spymaster, red_guesser, blue_spymaster, blue_guesser):
        self.setup_game()
        self.blue_team = {"spymaster": blue_spymaster, "guesser": blue_guesser}
        self.red_team = {"spymaster": red_spymaster, "guesser": red_guesser}
        self.winner = None
        self.win_type = None

    def setup_game(self):
        self.game_words = get_random_words(
            wordlist_path="assets/words.txt", num_words=25
        )
        self.start_team = random.choice(["red", "blue"])
        if self.start_team == "red":
            red_words, blue_words = 9, 8
        else:
            red_words, blue_words = 8, 9
        shuffled_words = random.sample(self.game_words, len(self.game_words))
        self.word_assignments = {
            "red": shuffled_words[:red_words],
            "blue": shuffled_words[red_words : red_words + blue_words],
            "neutral": shuffled_words[red_words + blue_words : 24],
            "assassin": [shuffled_words[24]],
        }
        self.turn_history = []

    def do_turn(self, team_color):
        print()
        if team_color == "blue":
            team = self.blue_team
            opponent_color = "red"
        elif team_color == "red":
            team = self.red_team
            opponent_color = "blue"

        words, num_cards = team["spymaster"].do_turn_spymaster()
        print(f"{team_color} Spymaster: {num_cards} words: {', '.join(words)}")
        guesses = team["guesser"].do_turn_guesser()
        self.turn_history.append({"spymaster": (words, num_cards), "guesser": guesses})

        for guess in guesses:
            print(f"{team_color} guesser: {guess} ...", end=" ")
            if guess in self.word_assignments[team_color]:  # Correct guess
                self.word_assignments[team_color].remove(guess)
                print("correct!")
            elif guess in self.word_assignments[opponent_color]:  # Incorrect guess, opponent's color
                self.word_assignments[opponent_color].remove(guess)
                print("incorrect! {guess} belonged to {opponent_color}!")
                break
            elif guess in self.word_assignments["neutral"]:  # Incorrect guess, neutral
                self.word_assignments["neutral"].remove(guess)
                print("incorrect! {guess} was neutral!")
                break
            elif guess in self.word_assignments["assassin"]:  # Incorrect guess, assassin
                self.word_assignments["assassin"].remove(guess)
                print("incorrect! {guess} was the assassin!")
                break

        # Current team lost
        if len(self.word_assignments[opponent_color]) == 0:
            self.winner = opponent_color
            self.win_type = "incorrect_guess"
            return

        if len(self.word_assignments["assassin"]) == 0:
            self.winner = opponent_color
            self.win_type = "assassin"
            return

        # Current team won
        if len(self.word_assignments["team"]) == 0:
            self.winner = team_color
            self.win_type = "correct_guess"
            return

    def run(self):
        current_turn = self.start_team
        while self.winner is None:
            self.do_turn(current_turn)
            current_turn = "blue" if current_turn == "red" else "red"
        print(f"Game over! Winner is team {self.winner}")
