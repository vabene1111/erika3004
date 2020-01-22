class Menu:

    def __init__(self, erika):
        self.erika = erika
        self.menu_running = True

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.erika.__exit__()

    def start_menu(self):
        self.erika.set_keyboard_echo(False)
        self.erika.move_right()
        self.erika.print_ascii("Menu")
        self.erika.move_down()

        while self.menu_running:
            inp = self.erika.read()
            programs = {
                "1": "tic_tac_toe",
                2: "test",
            }

            if programs.get(inp, None):
                self.run_program(programs.get(inp, None))

    def run_program(self, program):
        self.erika.print_ascii("Selected program " + program)
        self.menu_running = False
