"""Implementação de autômatos finitos."""
from typing import List, Dict


def load_automata(filename) -> tuple[List[str], List[str], List[tuple[str, str, str]], str, List[str]]:
    try:
        with open(filename, "rt") as input_file:
            alphabet: List[str] = input_file.readline().strip().split()
            state_list: List[str] = input_file.readline().strip().split()
            end_state_list: List[str] = input_file.readline().strip().split()
            start_state: str = input_file.readline().strip()
            transition_rule_list: List[tuple[str, str, str]] = []
            
            # region ESTADOS FINAIS NÃO ESTÃO PRESENTES NO CONJUNTO DE ESTADOS
            try:
                for end_state in end_state_list:
                    if end_state not in state_list:
                        raise ValueError("Estados finais não estão presentes no conjunto de estados")
            except ValueError as e:
                error(e)
            # endregion ESTADOS FINAIS NÃO ESTÃO PRESENTES NO CONJUNTO DE ESTADOS
            
            # region ESTADO INICIAL NÃO ESTÁ PRESENTE NO CONJUNTO DE ESTADOS
            try:
                if start_state not in state_list:
                    raise ValueError("Estado inicial não está presente no conjunto de estados")
            except ValueError as e:
                error(e)
            # endregion ESTADO INICIAL NÃO ESTÁ PRESENTE NO CONJUNTO DE ESTADOS

            for line in input_file:
                if line == "":
                    break
                else:
                    split_line: List[str] = line.split()
                    transition_rule_list.append((split_line[0], split_line[1], split_line[2]))
                    
            # region ERROS NA TRANSIÇÃO
            try:
                for transition_rule in transition_rule_list:
                    if transition_rule[2] not in state_list:
                        raise ValueError("Transição leva a estado que não está no conjunto de estados")
                    if transition_rule[0] not in state_list:
                        raise ValueError("Transição parte de estado que não está no conjunto de estados")
                    if transition_rule[1] not in alphabet and transition_rule[1] != "&":
                        raise ValueError("Transição utiliza símbolo inválido")
            except ValueError as e:
                error(e)
            # endregion ERROS NA TRANSIÇÃO

            return state_list, alphabet, transition_rule_list, start_state, end_state_list
    except FileNotFoundError as error:
        error(error)


def process(automata: tuple[List[str], List[str], List[tuple[str, str, str]], str, List[str]], words: List[str]) -> dict[str, str]:
    final_map: Dict[str: str] = {}
    
    for word in words:
        path: List[str] = [automata[3]]
        for symbol in word:
            transition_rule: tuple[str, str, str] = next(
                filter(lambda e: path[-1] == e[0] and symbol == e[1], automata[2]), None)
            if transition_rule is None:
                final_map[word] = "INVALIDA"
                break
            else:
                path.append(transition_rule[2])
        if word in final_map:
            pass
        elif path[-1] in automata[4]:
            final_map[word] = "ACEITA"
        else:
            final_map[word] = "REJEITA"
    return final_map


def convert_to_dfa(automata: tuple[List[str], List[str], List[tuple[str, str, str]], str, List[str]]) -> tuple[List[str], List[str], List[tuple[str, str, str]], str, List[str]]:
    states: List[str] = automata[0]
    alphabet: List[str] = automata[1]
    transition_rules: List[tuple[str, str, str]] = automata[2]
    start_state: str = automata[3]
    end_states: List[str] = automata[4]

    new_end_states: List[str] = []
    if start_state in end_states:  # VERIFICAR SE O ESTADO INICIAL TAMBÉM É UM ESTADO FINAL
        new_end_states.append(start_state)

    new_states: List[str] = [start_state]
    new_transition_rules: List[tuple[str, str, str]] = []
    queue_states: List[List[str]] = [[start_state]]
    states_already_test: List[List[str]] = []

    while len(queue_states) > 0:
        state_to_verify: List[str] = queue_states.pop(0)
        states_already_test.append(state_to_verify)
        transition_rules_of_new_state: List[tuple[str, str, str]] = list(
            filter(lambda e: e[0] in state_to_verify, transition_rules))

        for transition_rule in transition_rules_of_new_state.copy():
            if transition_rule[1] == "&":
                transition_rules_empty: List[tuple[str, str, str]] = list(
                    filter(lambda e: e[0] == transition_rule[2], transition_rules))
                transition_rules_of_new_state.extend(transition_rules_empty)
                transition_rules_of_new_state.remove(transition_rule)

        transition_rules_of_new_state = sorted(transition_rules_of_new_state)

        for symbol in alphabet:
            transition_rules_by_symbol = list(filter(lambda e: e[1] == symbol, transition_rules_of_new_state))
            new_state: str = ""
            states_to_append: List[str] = []
            for transition_rule in transition_rules_by_symbol:
                new_state += transition_rule[2]
                states_to_append.append(transition_rule[2])
            if new_state not in new_states:
                new_states.append(new_state)
                for end_state in end_states:
                    if end_state in new_state:
                        new_end_states.append(new_state)
            if states_to_append not in queue_states and states_to_append not in states_already_test:
                queue_states.append(states_to_append)
            new_transition_rules.append(("".join(state_to_verify), symbol, new_state))
    return new_states, alphabet, new_transition_rules, start_state, new_end_states


automata: tuple[List[str], List[str], List[tuple[str, str, str]], str, List[str]] = load_automata("../examples/06-nfa.txt")
automata = convert_to_dfa(automata)

print("Novos estados: ", automata[0])
print("Alfabeto: ", automata[1])
print("Novas regras de transição: ", automata[2])
print("Estado inicial: ", automata[3])
print("Lista de estados finais: ", automata[4])
"""Converte um NFA num DFA."""
