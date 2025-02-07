import re
import json
import fal_client

ALLOWED_PLAYERS = [
    "anthropic/claude-3.5-sonnet",
    "anthropic/claude-3-5-haiku",
    "anthropic/claude-3-haiku",
    "google/gemini-pro-1.5",
    "google/gemini-flash-1.5",
    "google/gemini-flash-1.5-8b",
    "meta-llama/llama-3.2-1b-instruct",
    "meta-llama/llama-3.2-3b-instruct",
    "meta-llama/llama-3.1-8b-instruct",
    "meta-llama/llama-3.1-70b-instruct",
    "openai/gpt-4o-mini",
    "openai/gpt-4o",
    # "deepseek/deepseek-r1",
]


class Player:
    def __init__(self, team_color: str, role: str, model: str):
        assert team_color in {
            "blue",
            "red",
        }, "team_color must be either 'blue' or 'red'"
        assert role in {
            "spymaster",
            "guesser",
        }, "role must be either 'spymaster' or 'guesser'"
        self.model = model
        self.team_color = team_color
        self.role = role

        self.sys_prompt = """
        You are playing Codenames. The game consists of two teams: Red Team and Blue Team. Each team has a Spymaster and a Guesser.
        Spymaster: Knows which words belong to their team, the opposing team, neutral words, and the assassin. Gives a one-word clue and a number indicating how many words are related to the clue. Example: "Ocean 2" means two words relate to "Ocean." Only respond with a single word and a number, separated by a space.
        Guesser: Tries to guess their team's words based on the clue. If they guess correctly, their team scores. If they guess an opposing team's word, the other team gains a point. If they guess a neutral word or an opponent's word, the turn ends. If they guess the assassin word, their team loses immediately. Respond with the number of words specified by the hint. Respond with the words, seperated by a space. Put the words you are most confident in first. Example: 'water boat'.
        Teams take turns. The goal is to guess all of your team's words before the opposing team while avoiding the assassin. The game ends when a team finds all their words or someone picks the assassin.
        """

    def do_turn_spymaster(self, word_assignments):
        correct_format = False
        num_tries = 0
        while not correct_format and num_tries < 5:
            result = fal_client.subscribe(
                "fal-ai/any-llm",
                arguments={
                    "model": self.model,
                    "system_prompt": self.sys_prompt,
                    "prompt": f"""You are the {self.team_color} team's spymaster. Think of a single word clue that allows your teammate to guess as many {self.team_color} words as possible. Avoid potential connections with the other remaining words. Avoid the assassin at all cost. Do not give hints which can easily be confused with the assassin.
The possible words and their assignments are as follows: {str(word_assignments)}.

Respond strictly in JSON format with the following structure:
{{
    "hint": "your_hint",
    "num_cards": number
}}

Your hint must not be a word already in the word list. Always think of a new word. ONLY RESPOND WITH THE JSON OBJECT NOTHING ELSE""",
                },
            )
            try:
                # gemini and gpt return a response like ```json{...}```, while llama and claude do not. This filters the response.
                cleaned_output = re.sub(
                    r"^```json|```$",
                    "",
                    result["output"].strip("```json").strip("```").strip(),
                ).strip()
                output = json.loads(cleaned_output)
                hint = output["hint"]
                num_cards = output["num_cards"]
                correct_format = True
            except Exception as e:
                print(
                    "[WARNING] spymaster did not return the correct format. Got error:",
                    e,
                    "Got:",
                    result["output"],
                )
                num_tries += 1
                hint, num_cards = "", 0

        return hint, num_cards

    def do_turn_guesser(self, clue_word, num_cards, left_over_words):
        correct_format = False
        num_tries = 0
        while not correct_format and num_tries < 5:
            result = fal_client.subscribe(
                "fal-ai/any-llm",
                arguments={
                    "model": self.model,
                    "system_prompt": self.sys_prompt,
                    "prompt": f"""You are the {self.team_color} team's guesser. The received clue word is "{clue_word}".
You must guess {num_cards} words based on this clue. Choose from any of the following words: {str(left_over_words)}.

Respond strictly in JSON format with the following structure:
{{
    "guesses": ["word1", "word2", "word3", ...]
}}

Make sure the words you guess are in the allowed words, never make up your own words and never guess the same word as the hint. Words must be in order from most certain to least certain. ONLY RESPOND WITH THE JSON OBJECT NOTHING ELSE""",
                },
            )
            try:
                # gemini and gpt return a response like ```json{...}```, while llama and claude do not. This filters the response.
                cleaned_output = re.sub(
                    r"^```json|```$",
                    "",
                    result["output"].strip("```json").strip("```").strip(),
                ).strip()
                output = json.loads(cleaned_output)
                guesses = output["guesses"]
                correct_format = True
            except Exception as e:
                print(
                    "[WARNING] guesser did not return the correct format. Got error:",
                    e,
                    "Got:",
                    result["output"],
                )
                num_tries += 1
                guesses = []

        return guesses
