class LeftLeftOne:
    def __init__(self, grammar):
        self.__grammar = grammar
        self.__first = {}
        self.__follow = {}

    def __config_first(self):
        non_terminals = self.__grammar.get_non_terminals()
        terminals = self.__grammar.get_terminals()

        for non_terminal in non_terminals:
            values = self.__grammar.get_production_by_non_terminal(non_terminal).get_values()

            for value in values:
                if value[0] in terminals:
                    if non_terminal not in self.__first.keys():
                        self.__first[non_terminal] = [value[0]]
                    else:
                        if value[0] not in self.__first[non_terminal]:
                            self.__first[non_terminal].append(value[0])
                elif non_terminal not in self.__first.keys():
                    self.__first[non_terminal] = []

    def get_first(self):
        non_terminals = self.__grammar.get_non_terminals()

        self.__config_first()
        current_first = self.__first
        new_first = {}

        while True:
            for non_terminal in non_terminals:
                if current_first[non_terminal]:
                    new_first[non_terminal] = current_first[non_terminal]
                else:
                    first_values = []
                    values = self.__grammar.get_production_by_non_terminal(non_terminal).get_values()

                    for value in values:
                        for first in current_first[value[0]]:
                            if first not in first_values:
                                first_values.append(first)

                    new_first[non_terminal] = first_values

            if current_first != new_first:
                current_first = new_first
            else:
                self.__first = current_first
                break

        return self.__first
