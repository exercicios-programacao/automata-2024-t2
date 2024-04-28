def load_automaton(filename):

    #aqui abre o arquivo e lê as linhas, se não houver transições vai apresentar mensagem de erro
    try:
        with open(filename, 'r') as file:
            linha = [line.strip() for line in file.readlines()]

        #aqui retiro as informações do arquivo 
        alfabeto = linha[0].split(" ")
        estados = linha[1].split(" ")
        estadoFinais = linha[2].split(" ")
        estadoInicial = linha[3].strip(" ")
        nodos = linha[4:]

        #cria a função da transição entre os estados
        transição = {estado: {} for estado in estados}

        for nodo in nodos:
            origem, simbolo, destino = nodo.split()
            if simbolo in transição[origem]:
                raise Exception("transição não encontrada")
            transição[origem][simbolo] = destino

        return estados, alfabeto, transição, estadoInicial, set(estadoFinais)
   
    except Exception as e:
        raise Exception (e)

def process(automato, words):
    estados, alfabeto, delta, estadoInicial, estadosFinais = automato
    
    processos = {}
    
    for word in words:
        estadoAtual = estadoInicial
        falso = False
        
        for simbolo in word:
            if simbolo not in alfabeto:
                estadoAtual[word] = "INVÁLIDA"
                falso = True
                break
            try:
                estadoAtual = delta[estadoAtual][simbolo]
            except Exception:
                estadoAtual[word] = "REJEITA"
                falso = True
                break
        
        if not falso:
            estadoAtual[word] = "ACEITA" if estadoAtual in estadosFinais else "REJEITA"
    
    return processos
