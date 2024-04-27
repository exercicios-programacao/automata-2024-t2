#lista das variáveis
class Automato:
    def __init__(self, estados, alfabeto, estadoInicial, estadosFinais, nodos):
        self.estados = estados
        self.alfabeto = alfabeto
        self.estadoInicial = estadoInicial
        self.estadosFinais = estadosFinais
        self.nodos = nodos

    def entradaValida(self, entrada):
        estadoAtual = self.estadoIncial # estado atual recebe estado inicial
        for simbolo in entrada: 
            if(estadoAtual, simbolo) not in self.nodos:
                return False
        estadoAtual = self.nodos[(estadoAtual, simbolo)][0]

        return estadoAtual in self.estadosFinais #faz a verificação do estado, se o estado final é um estado de aceitação ou não

def load_automata(filename):
    with open("01-simples.txt", "rt") as arquivo: #abre o arquivo para fazer a leitura de todas a linhas do arquivo
        linhas = arquivo.readlines()

# aqui faz um verificação se o arquivo tem ao menos 5 linhas, caso não tenha, é um arquivo inválido
    if len(linhas) < 5:
        raise ValueError("arquivo inválido")

#aqui faz a extração das linhas do arquivo
    estadoInicial = linhas[0]
    alfabeto = linhas[1].split(" ")
    estados = linhas[2].split(" ")
    estadosFinais = linhas[3].split(" ")
    #nodos = linhas[4:]
    nodos = {}

    for linha in linhas[4:]: #para cada linha de transição depois da 4 linha separa as linhas
        origem, simbolo, destino = linha.split("")
        if (origem, simbolo) not in nodos:
            nodos[(origem, simbolo)] = []
        nodos[(origem, simbolo)].append(destino)

    #aqui cria um objeto Automato com os dados lidos
    automato = Automato(estadoInicial, alfabeto, estados, estadosFinais, nodos)
    return automato

def main():
    file = input("Digite o nome do arquivo que contém o autômato: ")
    try:
        automato = load_automata(file)
        if automato.entradaValida(file):
            print("ACEITA")
        else:
            print("REJEITA")
    except Exception as e:
        print("Arquivo Inválido")

if __name__ == "__main__":
    main()
