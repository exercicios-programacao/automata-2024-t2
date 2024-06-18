"""Implementação de autômatos finitos."""


def load_automata(filename: str):
    """
    Lê os dados de um autômato finito a partir de um arquivo.

    A estsrutura do arquivo deve ser:

    <lista de símbolos do alfabeto, separados por espaço (' ')>
    <lista de nomes de estados>
    <lista de nomes de estados finais>
    <nome do estado inicial>
    <lista de regras de transição, com "origem símbolo destino">

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
    with open(filename, "rt", encoding="utf-8") as arquivo:
        lines = arquivo.readlines()
        sigma = lines[0].strip().split()
        sigma.append('&')
        q = lines[1].strip().split()
        f = lines[2].strip().split()
        for estado in f:
            if estado not in q:
                raise ValueError("Estado final não está na lista de estados.")
        q0 = lines[3].strip()
        if q0 not in q:
            raise ValueError("O estado inicial não está na lista de estados.")
        delta = {}
        for linha in lines[4:]:
            origem, simbolo, destino = linha.strip().split()
            if origem not in q or destino not in q or (simbolo not in sigma and simbolo != '&'):
                raise ValueError("Transição inválida")
            if origem not in delta:
                delta[origem] = {}
            if simbolo not in delta[origem]:
                delta[origem][simbolo] = []
            delta[origem][simbolo].append(destino)
    return q, sigma, delta, q0, f


def process(automata, words):
    """
    Processa a lista de palavras e retora o resultado.

    Os resultados válidos são ACEITA, REJEITA, INVALIDA.
    """
    q, sigma, delta, q0, f = automata

    for estado in delta:
        for simbolo in delta[estado]:
            if len(delta[estado][simbolo]) > 1:
                automata = convert_to_dfa(automata)
                q, sigma, delta, q0, f = automata
                break
        else:
            continue
        break

    resultado = {}

    for word in words:
        letras = list(word)
        estado_invalido = False

        for letra in letras:
            if letra not in sigma and letra != '&':
                resultado[word] = 'INVALIDA'
                estado_invalido = True
                break

        if not estado_invalido:
            atual = q0
            for letra in letras:
                if letra == '&':
                    while '&' in delta.get(atual, {}):
                        atual = delta[atual]['&'][0]
                elif letra in delta.get(atual, {}):
                    atual = delta[atual][letra][0]
                else:
                    resultado[word] = 'REJEITA'
                    break
            else:
                if atual in f:
                    resultado[word] = 'ACEITA'
                else:
                    resultado[word] = 'REJEITA'

        if estado_invalido and atual in q:
            resultado[word] = 'INVALIDA'
        elif not estado_invalido and atual not in q:
            resultado[word] = 'REJEITA'
    return resultado


def convert_to_dfa(automata):
    """Convert um NFA num DFA."""
    q, sigma, delta, q0, f = automata
    dfa_q = set()
    dfa_delta = {}
    dfa_f = []
    dfa_q0 = (q0,)
    estados_pendentes = [dfa_q0]
    estados_processados = set()

    while estados_pendentes:
        estado_atual = estados_pendentes.pop()
        estados_processados.add(estado_atual)
        dfa_q.add(estado_atual)

        for simbolo in sigma:
            if simbolo == '&':
                continue
            novos_estados = set()
            for sub_estado in estado_atual:
                if simbolo in delta.get(sub_estado, {}):
                    novos_estados.update(delta[sub_estado][simbolo])
                if '&' in delta.get(sub_estado, {}):
                    novos_estados.update(delta[sub_estado]['&'])
            novos_estados = tuple(sorted(novos_estados))
            if novos_estados:
                if novos_estados not in estados_processados and novos_estados not in estados_pendentes:
                    estados_pendentes.append(novos_estados)
                if estado_atual not in dfa_delta:
                    dfa_delta[estado_atual] = {}
                dfa_delta[estado_atual][simbolo] = novos_estados
                if novos_estados not in q:
                    q.append(novos_estados)

    for estado in dfa_q:
        if any(sub_estado in f for sub_estado in estado):
            dfa_f.append(estado)

    return q, sigma, dfa_delta, q0, dfa_f
