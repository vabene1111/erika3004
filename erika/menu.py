import os
from time import sleep

from erika.TicTacToe import TicTacToe


class Menu:

    def __init__(self, erika):
        self.erika = erika
        self.menu_running = True
        self.program_running = False

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.erika.__exit__()

    def start_menu(self):
        programs = {
            "1": "tic_tac_toe",
            "2": "test",
            "q": "quit"
        }

        self.erika.set_keyboard_echo(False)
        self.erika.print_ascii("\nErika Menu v0.0.0.0.1\n")

        for key, program in programs.items():
            self.erika.print_ascii(key + " - " + program + "\n")

        for x in range(0, 5):
            self.erika.move_down()

        while self.menu_running:
            inp = self.erika.read()

            if programs.get(inp, None) and not self.program_running:
                self.run_program(programs.get(inp, None))

    def run_program(self, program):
        self.erika.set_keyboard_echo(True)
        self.program_running = True

        for x in range(0, 5):
            self.erika.move_up()

        if program == "quit":
            self.menu_running = False
        if program == "tic_tac_toe":
            with TicTacToe(self.erika) as game:
                game.start_game()

        self.program_running = False
