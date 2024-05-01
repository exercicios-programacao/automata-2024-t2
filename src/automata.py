"""Implementação de autômatos finitos."""

""" load_automata(filename: str): -> tuple(Q, Sigma, delta, q0, F)"""
def get_F(F_list):
    F_return = []
    for F in F_list:
        F_return.append(F.strip().split(" "))
    return F_return

def get_transitional_Q(F):
    transitional_Q = []
    for element_F in F:
        element_Q = element_F[1]
        transitional_Q.append(element_Q)
    return transitional_Q

def get_transitional_state(F):
    transitional_state = []
    for element_F in F:
        transitional_state.append(element_F[0])
        transitional_state.append(element_F[2])
    return transitional_state

def automata_validate(automata):
    Q = automata[0]
    Sigma = automata[1]
    delta = automata[2]
    q0 = automata[3]
    F = automata[4]

    errorMsg = []

    if not q0 in Sigma:
        errorMsg.append("Estado inicial "+q0+" não está na lista de estados")
    
    for end_state in delta:
        if not end_state in Sigma:
            errorMsg.append("Estado final "+end_state+" não está na lista de estados")
    
    for element_Q in get_transitional_Q(F):
        if not element_Q in Q and element_Q != "&" :
            errorMsg.append("Letra de transição "+element_Q+" não está no alfabeto")

    for element_state in get_transitional_state(F):
        if not element_state in Sigma:
            errorMsg.append("Estado de transição "+element_state+" não está na lista de estados")
    
    if not q0 == automata[1][0]:
        errorMsg.append("Estado inicial de transição "+automata[1][0]+" não é o estado inicial "+q0)        

    if not errorMsg:
        return "Automato Válido"
    else:
        return '; '.join(errorMsg)
    
        
def load_automata(filename):
    """
    Lê os dados de um autômato finito a partir de um arquivo.

    A estsrutura do arquivo deve ser:

    <lista de símbolos do alfabeto, separados por espaço (' ')> -> Q
    <lista de nomes de estados> -> Sigma
    <lista de nomes de estados finais> -> delta
    <nome do estado inicial> -> q0
    <lista de regras de transição, com "origem símbolo destino"> -> F

    Um exemplo de arquivo válido é:

    ```
    a b
    q0 q1 q2 q3
    q0 q3
    q0
    q0 a q1
    q0 b q2
    q1 a q0
    q1 b q3
    q2 a q3
    q2 b q0
    q3 a q1
    q3 b q2
    ```

    Caso o arquivo seja inválido uma exceção Exception é gerada.

    """


    try:
        with open(filename, "rt") as arquivo:
            lines = arquivo.readlines()
            pass
    except:
        print("Arquivo inválido")
    
    Q = lines[0].strip().split(" ")
    Sigma = lines[1].strip().split(" ")
    delta = lines[2].strip().split(" ")
    q0 = lines[3].strip()
    F = get_F(lines[4:])

    tuple = (Q, Sigma, delta, q0, F)

    if automata_validate(tuple) == "Automato Válido":
        return tuple
    else:
        raise Exception( automata_validate(tuple))

def get_nextState(state, letter, F):
    for transition_rule in F:
        if transition_rule[0] == state and transition_rule[1] == letter:
            return transition_rule[2]
    return None

def processWord(word, automata):
    

    Q = automata[0]
    Sigma = automata[1]
    delta = automata[2]
    q0 = automata[3]
    F = automata[4]

    curr_state = q0

    i = -1
    for letter in word:
        i += 1
        if not letter in Q:
            #print("INVALIDA")
            return "INVALIDA"
        previous_state = curr_state
        curr_state = get_nextState(curr_state, letter, F)
        if curr_state is None:
            #print("REJEITA")
            return "REJEITA"
        if i != len(word) - 1:
            pass
        #    print(previous_state+", "+letter)
        #    print("|")
        #    print("v")
        else:
            print(curr_state+", "+letter)
            if curr_state in delta:
                #print("ACEITA")
                return "ACEITA"
            else:
                #print("REJEITA")
                return "REJEITA"
    
    if word == "" and q0 in delta:
        return "ACEITA"
    else:
        return "REJEITA"




def process(automata, words):
    """
    Processa a lista de palavras e retora o resultado.
    
    Os resultados válidos são ACEITA, REJEITA, INVALIDA.
    """

    print(automata_validate(automata))

    if automata_validate(automata) == "Automato Válido":
        dict = {}
        for word in words:
            #print("\nProcessando palavra "+word+"--------------------------------------------------")
            dict[word] = processWord(word, automata)
        return dict
    else:
        return "INVALIDA"


def get_nextState_NFA(state, letter, F):
    states_tramsition = []
    for transition_rule in F:
        if transition_rule[1] == '&':
            return "".join([transition_rule[0],transition_rule[2]])
        if transition_rule[0] == state and transition_rule[1] == letter and transition_rule[2] not in states_tramsition:
            states_tramsition.append(transition_rule[2])
        if transition_rule[0] == state and transition_rule[1] == '&' and transition_rule[2] not in states_tramsition:
            states_tramsition.append(transition_rule[2])

    if states_tramsition == []:
        return state
    else:
        return "".join(states_tramsition)
def convert_to_dfa(automata):
    Q = automata[0]     # -> <lista de símbolos do alfabeto, separados por espaço (' ')>
    Sigma = automata[1] # -> <lista de nomes de estados>
    delta = automata[2] # -> <lista de nomes de estados finais>
    q0 = automata[3]    # -> <nome do estado inicial>
    F = automata[4]     # -> <lista de regras de transição, com "origem símbolo destino">
    
    new_Q = Q.copy()
    new_Sigma = []
    new_delta = []
    new_q0 = ""
    new_F = []

    # -> Passo 1: Definir novo Sigma
    new_Sigma.append(q0)
    for transition_rule in F:
        nextState = get_nextState_NFA(transition_rule[0],transition_rule[1], F)
        if nextState not in new_Sigma:
            new_Sigma.append(nextState)
    
    deleted_in_new_Sigma = []
    for state_1 in new_Sigma:
        for state_2 in new_Sigma:
            if state_1 in state_2 and state_1 != state_2:
                deleted_in_new_Sigma.append(state_1)
    
    for deleted_state in deleted_in_new_Sigma:
        new_Sigma.remove(deleted_state)

    # -> Passo 2: Definir novo delta

    for state in delta:
        for new_state in new_Sigma:
            if state in new_state:
                new_delta.append(new_state)

    # -> Passo 3: Definir novo q0

    for new_state in new_Sigma:
        if q0 in new_state:
            new_q0 = new_state
            
    # -> Passo 4: Definir novo F

    for transition_rule in F:
        initial_state = transition_rule[0]
        letter = transition_rule[1]
        final_state = transition_rule[2]
        for new_state in new_Sigma:
            if initial_state in new_state:
                initial_state = new_state
                break
        for new_state in new_Sigma:
            if final_state in new_state:
                final_state = new_state
        new_F.append([initial_state, letter, final_state])

    deleted_index_new_F = []   

    for i, cmp_transition_rule_1 in enumerate(new_F):
        for j, cmp_transition_rule_2 in enumerate(new_F):
            if cmp_transition_rule_1 == cmp_transition_rule_2 and i != j:
                deleted_index_new_F.append(j)

    for deleted_index in deleted_index_new_F:
        del new_F[deleted_index]
    
    print(new_Q)       
    print(new_Sigma)
    print(new_delta)
    print(new_q0)
    print(new_F)

    return (new_Q, new_Sigma, new_delta, new_q0, new_F)

convert_to_dfa(load_automata("./examples/06-nfa.txt"))
convert_to_dfa(load_automata("./examples/07-nfa.txt"))
convert_to_dfa(load_automata("./examples/08-nfa.txt"))
convert_to_dfa(load_automata("./examples/09-nfa.txt"))
convert_to_dfa(load_automata("./examples/10-nfa.txt"))
