from ll1.LeftLeftOne import LeftLeftOne
from grammar.grammar import Grammar


def main():
    grammar = Grammar()
    grammar.config_grammar_from_file("grammar/config/grammar_config_1.txt")
    ll1 = LeftLeftOne(grammar)
    first = ll1.get_first()
    print(first)

    print(ll1.get_follow())


if __name__ == '__main__':
    main()
