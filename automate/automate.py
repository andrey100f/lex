from automate.transition import Transition
from grammar.production import Production
from grammar.grammar import Grammar


class Automate:
    def __init__(self):
        self.__states = []
        self.__alphabet = []
        self.__transitions = []
        self.__initial_state = None
        self.__final_state = None

    def config_automate_from_grammar(self, states, alphabet, transitions, initial_state, final_state, filename):
        for letter in alphabet:
            self.__alphabet.append(letter)
        for state in states:
            self.__states.append(state)
        for transition in transitions:
            self.__transitions.append(transition)
        self.__initial_state = initial_state
        self.__final_state = final_state

        self.__create_config_file(filename)

    def __create_config_file(self, filename):
        with open(filename, "w") as file:
            line = ""
            for letter in self.__alphabet:
                line += letter
                line += " "
            line = line.strip()
            file.write(line)
            file.write("\n")

            line = ""
            for state in self.__states:
                line += state
                line += " "
            line = line.strip()
            file.write(line)
            file.write("\n")

            file.write(self.__initial_state)
            file.write("\n")

            file.write(self.__final_state)
            file.write("\n")

            for transition in self.__transitions:
                line = str(transition)
                file.write(line)
                file.write("\n")

    def config_automate_from_file(self, filename):
        with open(filename, "r") as file:
            line_number = 0
            for line in file:
                line_number += 1
                if line_number == 1:
                    self.__add_elements(line, "alphabet")
                elif line_number == 2:
                    self.__add_elements(line, "states")
                elif line_number == 3:
                    line = line.strip("\n")
                    self.__initial_state = line
                elif line_number == 4:
                    line = line.strip("\n")
                    self.__final_state = line
                else:
                    self.__add_transitions(line)

    def __add_elements(self, line, list_to_add):
        line = line.strip("\n")
        terminals = line.split(" ")

        if list_to_add == "alphabet":
            grammar_element = self.__alphabet
        else:
            grammar_element = self.__states

        for terminal in terminals:
            grammar_element.append(terminal)

    def __add_transitions(self, line):
        line = line.strip("\n")
        transition = Transition()
        transition.set_transition(line)
        self.__transitions.append(transition)

    def __get_transition(self, source_state, symbol):
        for transition in self.__transitions:
            if transition.get_source_state() == source_state and transition.get_symbol() == symbol:
                return transition

        return None

    def get_alphabet(self):
        return self.__alphabet

    def get_states(self):
        return self.__states

    def get_initial_state(self):
        return self.__initial_state

    def get_final_state(self):
        return self.__final_state

    def get_transitions(self):
        return self.__transitions

    def get_next_state(self, source_state, symbol):
        next_states = []

        for transition in self.__transitions:
            if transition.get_source_state() == source_state and transition.get_symbol() == symbol:
                next_states.append(transition.get_next_state())

        return next_states

    def check_sequence(self, sequence):
        if len(sequence) == 0:
            return False

        current_state = self.__initial_state

        length = 0
        for letter in sequence:
            length += 1
            transition = self.__get_transition(current_state, letter)

            if transition is None:
                return False

            current_state = transition.get_next_state()

        if current_state == self.__final_state:
            return True
        elif length == len(sequence):
            return True

        return False

    def convert_to_grammar(self, filename):
        grammar = Grammar()

        non_terminals = []
        for non_terminal in self.__states:
            non_terminals.append(non_terminal)

        start_symbol = self.__initial_state
        end_symbol = self.__final_state

        terminals = []
        for terminal in self.__alphabet:
            terminals.append(terminal)

        productions = []
        founded_productions = {}
        for transition in self.__transitions:
            if transition.get_source_state() != transition.get_next_state():
                if transition.get_source_state() not in founded_productions.keys():
                    founded_productions[transition.get_source_state()] = []
                    founded_productions[transition.get_source_state()].append(transition.get_next_state())
                elif transition.get_next_state() not in founded_productions[transition.get_source_state()]:
                    founded_productions[transition.get_source_state()].append(transition.get_next_state())

                if transition.get_source_state() != self.__initial_state:
                    if transition.get_next_state() not in founded_productions.keys():
                        founded_productions[transition.get_next_state()] = []
                        founded_productions[transition.get_next_state()].append(transition.get_symbol())
                    elif transition.get_symbol() not in founded_productions[transition.get_next_state()]:
                        founded_productions[transition.get_next_state()].append(transition.get_symbol())
            else:
                if transition.get_source_state() not in founded_productions.keys():
                    founded_productions[transition.get_source_state()] = []
                    founded_productions[transition.get_source_state()].append(transition.get_source_state() + transition.get_symbol())
                else:
                    founded_productions[transition.get_source_state()].append(
                        transition.get_source_state() + transition.get_symbol())

        for key, value in founded_productions.items():
            symbol = key
            list_of_values = " | ".join(value)
            line = symbol + " -> " + list_of_values
            production = Production()
            production.set_production(line)
            productions.append(production)

        grammar.config_grammar_from_automate(non_terminals, terminals, start_symbol, end_symbol, productions, filename)

        return grammar

    def print_automate(self):
        print("-------------------------------------------------------------------------------------------------------")
        print(f"Multimea starilor este: {self.__states}")
        print(f"Alfabetul este: {self.__alphabet}")
        print(f"Starea initiala este: {self.__initial_state}")
        print(f"Starea finala este: {self.__final_state}")
        print("Multimea tranzitiilor este: ")
        for transition in self.__transitions:
            print(transition)
