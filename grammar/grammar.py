from grammar.production import Production


class Grammar:
    def __init__(self):
        self.__non_terminals = []
        self.__terminals = []
        self.__productions = []
        self.__start_symbol = None
        self.__end_symbol = None

    def config_grammar_from_automate(self, non_terminals, terminals, start_symbol, end_symbol, productions, filename):
        for non_terminal in non_terminals:
            self.__non_terminals.append(non_terminal)
        for terminal in terminals:
            self.__terminals.append(terminal)
        for production in productions:
            self.__productions.append(production)
        self.__start_symbol = start_symbol
        self.__end_symbol = end_symbol

        self.__create_config_file(filename)

    def __create_config_file(self, filename):
        with open(filename, "w") as file:
            line = ""
            for letter in self.__terminals:
                line += letter
                line += " "
            line = line.strip()
            file.write(line)
            file.write("\n")

            line = ""
            for letter in self.__non_terminals:
                line += letter
                line += " "
            line = line.strip()
            file.write(line)
            file.write("\n")

            file.write(self.__start_symbol)
            file.write("\n")

            file.write(self.__end_symbol)
            file.write("\n")

            for production in self.__productions:
                symbol = production.get_symbol()
                values = " | ".join(production.get_values())
                line = symbol + " -> " + values
                file.write(line)
                file.write("\n")

    def config_grammar_from_file(self, filename):
        with open(filename, "r") as file:
            line_number = 0
            for line in file:
                line_number += 1
                if line_number == 1:
                    self.add_elements(line, "terminals")
                elif line_number == 2:
                    self.add_elements(line, "non_terminals")
                elif line_number == 3:
                    line = line.strip("\n")
                    self.__start_symbol = line
                elif line_number == 4:
                    line = line.strip("\n")
                    self.__end_symbol = line
                else:
                    self.__add_productions(line)

    def add_elements(self, line, list_to_add):
        line = line.strip("\n")
        terminals = line.split(" ")

        if list_to_add == "terminals":
            grammar_element = self.__terminals
        else:
            grammar_element = self.__non_terminals

        for terminal in terminals:
            grammar_element.append(terminal)

    def __add_productions(self, line):
        line = line.strip("\n")
        production = Production()
        production.set_production(line)
        self.__productions.append(production)

    def get_productions(self):
        return self.__productions

    def get_production_by_non_terminal(self, non_terminal):
        result = None
        for production in self.__productions:
            symbol = production.get_symbol()
            if symbol == non_terminal:
                result = production
        return result

    def get_start_symbol(self):
        return self.__start_symbol

    def get_terminals(self):
        return self.__terminals

    def get_non_terminals(self):
        return self.__non_terminals

    def get_end_symbol(self):
        return self.__end_symbol

    def check_regular(self):
        nr_start_symbol = 0
        for production in self.__productions:
            if production.get_symbol() == self.__start_symbol:
                nr_start_symbol += 1
        if nr_start_symbol > 1:
            return False

        for production in self.__productions:
            for value in production.get_values():
                reversed_value = value[::-1]
                if reversed_value in production.get_values() and len(value) > 1:
                    return False

            if production.get_symbol() not in self.__non_terminals:
                return False

            for symbol in production.get_values():
                for letter in symbol:
                    if letter not in self.__terminals and letter not in self.__non_terminals:
                        return False

        return True

    def convert_to_finite_automate(self, filename):
        if self.check_regular() is False:
            return None

        from automate.automate import Automate
        from automate.transition import Transition

        automate = Automate()

        states = []
        for state in self.__non_terminals:
            states.append(state)

        initial_state = self.__start_symbol
        final_state = self.__end_symbol

        alphabet = []
        for letter in self.__terminals:
            alphabet.append(letter)

        transitions = []
        for production in self.__productions:
            for value in production.get_values():
                if len(value) != 1:
                    transition = Transition()
                    line = production.get_symbol() + " " + value[1] + " " + value[0]
                    transition.set_transition(line)
                    transitions.append(transition)
                else:
                    if value in self.__non_terminals:
                        prod = self.get_production_by_non_terminal(value)
                        for val in prod.get_values():
                            if len(val) != 1:
                                transition = Transition()
                                line = production.get_symbol() + " " + val[1] + " " + val[0]
                                transition.set_transition(line)
                                transitions.append(transition)
                            elif val not in self.__non_terminals:
                                transition = Transition()
                                line = production.get_symbol() + " " + val + " " + self.__end_symbol
                                transition.set_transition(line)
                                transitions.append(transition)

        automate.config_automate_from_grammar(states, alphabet, transitions, initial_state, final_state, filename)

        return automate

    def print_grammar(self):
        print("-------------------------------------------------------------------------------------------------------")
        print(f"Multimea non-terminalelor este: {self.__non_terminals}")
        print(f"Multimea terminalelor este: {self.__terminals}")
        print(f"Simbolul de start este: {self.__start_symbol}")
        print(f"Simbolul final este: {self.__end_symbol}")
        print("Multimea productiilor este: ")
        for production in self.__productions:
            print(production)
