
class Player:
    def __init__(self, team: str, role: str):
        assert team in {"blue", "red"}, "team must be either 'blue' or 'red'"
        assert role in {"spymaster", "guesser"}, "role must be either 'spymaster' or 'guesser'"
        self.team = team
        self.role = role

        self.sys_prompt = ""

    def do_turn_spymaster(self):
        raise NotImplementedError

    def do_turn_guesser(self):
        raise NotImplementedError

    def do_turn(self):
        if self.role == "spymaster":
            self.do_turn_spymaster()
        if self.role == "guesser":
            self.do_turn_guesser()


class GPT4oPlayer(Player):
    def do_turn_spymaster(self):
        raise NotImplementedError

    def do_turn_guesser(self):
        raise NotImplementedError
