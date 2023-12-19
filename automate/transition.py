class Transition:
    def __init__(self):
        self.__source_state = None
        self.__next_state = None
        self.__symbol = None

    def set_transition(self, line):
        source_state, symbol, next_state = line.split(" ")

        self.__source_state = source_state
        self.__symbol = symbol
        self.__next_state = next_state

    def get_source_state(self):
        return self.__source_state

    def get_symbol(self):
        return self.__symbol

    def get_next_state(self):
        return self.__next_state

    def __str__(self):
        return f"{self.__source_state} {self.__symbol} {self.__next_state}"
