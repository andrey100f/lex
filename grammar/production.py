class Production:
    def __init__(self):
        self.__symbol = None
        self.__values = []

    def set_production(self, line):
        production_symbol, production_values = line.split("->")

        production_symbol = production_symbol.strip()
        self.__symbol = production_symbol

        production_values = production_values.split("|")
        for value in production_values:
            value = value.strip()
            self.__values.append(value)

    def get_values(self):
        return self.__values

    def get_symbol(self):
        return self.__symbol

    def __str__(self):
        return f'{self.__symbol} -> {self.__values}'
