from grammar.grammar import Grammar
from ll1.LeftLeftOne import LeftLeftOne


class UI:
    def __init__(self, filename):
        self.__grammar = Grammar()
        self.__ll1 = LeftLeftOne(self.__grammar)
        self.__grammar.config_grammar_from_file(filename)

    def display_menu(self):
        while True:
            print("")
            print("(1) Afisare terminale.")
            print("(2) Afisare non-terminale.")
            print("(3) Afisare productii.")
            print("(4) Afisare productii ale unui non-terminal.")
            print("(5) Afisare simbol de start.")
            print("(6) Verificare gramatica regulara.")
            print("(7) Conversie in automat.")
            print("(8) Afisare FIRST.")
            print("(9) Afisare FOLLOW.")
            print("(x) Iesire.")

            choice = input("Dati optiunea: ")
            if choice == "1":
                terminals = self.__grammar.get_terminals()

                print(f"Multimea terminalelor este: {terminals}")
            elif choice == "2":
                non_terminals = self.__grammar.get_non_terminals()

                print(f"Multimea non-terminalelor este: {non_terminals}")
            elif choice == "3":
                productions = self.__grammar.get_productions()

                print("Multimea productiilor este: ")
                for production in productions:
                    print(production)
            elif choice == "4":
                non_terminal = input("Dati non-terminalul: ")

                production = self.__grammar.get_production_by_non_terminal(non_terminal)

                if production is None:
                    print("Non-terminalul nu este valid!!")
                else:
                    print(f"Productia este: {production}")
            elif choice == "5":
                start_symbol = self.__grammar.get_start_symbol()

                print(f"Simbolul de start este: {start_symbol}")
            elif choice == "6":
                is_regular = self.__grammar.check_regular()

                if is_regular is True:
                    print("Gramatica este regulara!!")
                else:
                    print("Granatica nu este regulara!!")

            elif choice == "7":
                filename = "grammar/result_automate_config.txt"
                automate = self.__grammar.convert_to_finite_automate(filename)

                if automate is None:
                    print("Nu s-a putut configura automatul deoarece granatica nu este regulara!")
                else:
                    print(f"Fisierul de configurare pentru automatul generat este: {filename}")
                    print("Automatul generat este: ")
                    automate.print_automate()
            elif choice == "8":
                first = self.__ll1.get_first()

                print("Multimea FIRST este: ")
                for key in first.keys():
                    print(f"FIRST({key}) = {first[key]}")
            elif choice == "9":
                follow = self.__ll1.get_follow()

                print("Multimea FOLLOW este: ")
                for key in follow.keys():
                    print(f"FOLLOW({key}) = {follow[key]}")
            elif choice == "x":
                break
            else:
                print("Optiune gresita!! Reincercati...")
