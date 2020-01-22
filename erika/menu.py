class Menu:

    def __init__(self, erika):
        self.erika = erika

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.erika.__exit__()

    def start_menu(self):
        self.erika.set_keyboard_echo(False)
        self.erika.move_right()
        self.erika.print_ascii("Menu")
        self.erika.move_down()

        while True:
            inp = self.erika.read()
            if inp:
                self.erika.print_ascii("Entry selected was " + inp)
            break

        self.erika.set_keyboard_echo(True)
