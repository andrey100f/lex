from grammar.grammar import Grammar


def main():
    grammar = Grammar()
    grammar.config_grammar_from_file("grammar/grammar_config.txt")
    new_grammar = grammar.eliminate_left_recursion(grammar)
    new_grammar.print_grammar()


if __name__ == '__main__':
    main()
