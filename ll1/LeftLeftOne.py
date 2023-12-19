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

    def __config_follow(self):
        non_terminals = self.__grammar.get_non_terminals()

        for non_terminal in non_terminals:
            if  non_terminal == self.__grammar.get_start_symbol():
                self.__follow[non_terminal] = ["E"]
            else:
                self.__follow[non_terminal] = []

    def get_follow(self):
        self.__config_follow()

        non_terminals = self.__grammar.get_non_terminals()
        terminals = self.__grammar.get_terminals()
        current_follow = self.__follow
        new_follow = {}

        while True:
            for non_terminal in non_terminals:
                list_of_values = []

                if self.__follow[non_terminal]:
                    for value in current_follow[non_terminal]:
                        list_of_values.append(value)

                productions = self.__grammar.get_production_containing_non_terminal(non_terminal)
                for production in productions:
                    production_values = production.get_values()
                    production_symbol = production.get_symbol()

                    for value in production_values:
                        if non_terminal in value and (non_terminal + "'") not in value:
                            if non_terminal + "'" in value:
                                value_to_search = non_terminal + "'"
                            else:
                                value_to_search = non_terminal
                            index = value.find(value_to_search) + len(value_to_search)

                            if index == len(value):
                                if "E" not in list_of_values:
                                    list_of_values.append("E")

                                follow_start_symbol_to_add = current_follow[production_symbol]

                                for follow_element in follow_start_symbol_to_add:
                                    if follow_element not in list_of_values:
                                        list_of_values.append(follow_element)

                            else:
                                next_value = value[index]

                                if next_value in terminals:
                                    if next_value not in list_of_values:
                                        list_of_values.append(next_value)
                                else:
                                    for first_value in self.__first[next_value]:
                                        if first_value not in list_of_values:
                                            list_of_values.append(first_value)

                                    if "E" in self.__first[next_value]:
                                        follow_start_symbol_to_add = current_follow[production_symbol]

                                        for follow_element in follow_start_symbol_to_add:
                                            if follow_element not in list_of_values:
                                                list_of_values.append(follow_element)

                new_follow[non_terminal] = list_of_values

            if new_follow != current_follow:
                current_follow = new_follow
            else:
                self.__follow = current_follow
                break

        return self.__follow
