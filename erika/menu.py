import os
from time import sleep

from erika.TicTacToe import TicTacToe

SCROLL_DOWN_ROWS = 5
PROGRAMS = {
    "1": "tic_tac_toe",
    "2": "test",
    "q": "quit"
}

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
        self.print_menu()
        while self.menu_running:
            inp = self.erika.read()

            if PROGRAMS.get(inp, None) and not self.program_running:
                self.run_program(PROGRAMS.get(inp, None))

    def print_menu(self):
        self.erika.set_keyboard_echo(False)
        self.erika.print_ascii("\nErika Menu v0.0.0.0.1\n")

        for key, program in PROGRAMS.items():
            self.erika.print_ascii(key + " - " + program + "\n")

        for x in range(0, SCROLL_DOWN_ROWS):
            self.erika.move_down()

    def run_program(self, program):
        self.erika.set_keyboard_echo(True)
        self.program_running = True

        for x in range(0, SCROLL_DOWN_ROWS):
            self.erika.move_up()

        if program == "quit":
            self.erika.print_ascii("\n")
            self.menu_running = False

        if program == "tic_tac_toe":
            with TicTacToe(self.erika) as game:
                game.start_game()

        sleep(2)
        self.print_menu()
        self.program_running = False
