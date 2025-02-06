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
    "deepseek/deepseek-r1",
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
        self.model
        self.team_color = team_color
        self.role = role

        self.sys_prompt = ""

    def do_turn_spymaster(self, word_assignments):
        result = fal_client.subscribe(
            "fal-ai/any-llm",
            arguments={
                "model": self.model,
                "system_prompt": self.sys_prompt,
                "prompt": f"You are the {self.team_color} team's spymaster. Think of a single word clue that allows your team mate guess as many {self.team_color} words as possible. Avoid potential connections with the other remaining words.",
            },
        )
        print(result)

        # TODO: parse result and verify it is a json object.

        return result

    def do_turn_guesser(self, clue_word):
        result = fal_client.subscribe(
            "fal-ai/any-llm",
            arguments={
                "model": self.model,
                "system_prompt": self.sys_prompt,
                "prompt": f"You are the {self.team_color} team's guesser. The received clue word is {clue_word}. Return your guesses in a json list, with words being in order of which you are most certain of, to least",
            },
        )
        print(result)

        # TODO: parse result and verify it is a json object.

        return result
