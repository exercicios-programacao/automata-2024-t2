def load_automata(filename):
	if isinstance(filename, str):
            try:
                with open(filename) as arquivo:
                    linhas = arquivo.readlines()
                    # faz a leitura das linhas e verifica se o arquivo possui 5 linhas
        
                    # inicializa uma lista para armazenar as transições
                    transicoes = []
        
                    if len(linhas) < 5:
                        raise Exception("Arquivo não contém suficientes linhas para representar um autômato")
                    # faz a extração das informações do arquivo na parte do alfabeto
                    alfabeto = tuple(linhas[0].strip().split(" "))
                    estados = tuple(linhas[1].strip().split(" "))
                    # faz a extração dos estados finais, garantindo que estão presentes nos estados,
                    #se não retorna erro que os estados não estão presentes
                    estadosFinais = tuple(estado for estado in linhas[2].strip().split(" ") if estado in estados)
                    estadoIncial = linhas[3].strip() 

                    # processa as linhas restantes como regras de transição
                    for linha in linhas[4:]:
                        transicao = tuple(linha.strip().split(" "))

                    if len(transicao) < 3 or transicao[0] not in estados or transicao[1] not in alfabeto or transicao[2] not in estados:
                        raise Exception("Transição não determinística não encontrada")
                    print(f"{transicao} é o correto.")
        
                    # Adiciona a regra de transição à lista de transições
                    transicoes.append(transicao)
        
                    return{
                        "Alfabeto": alfabeto,
                        "Estado:": estados,
                        "Estados Finais: ": estadosFinais, 
                        "Estado Inicial": estadoIncial,
                        "Transição: ": transicoes,
                    }
            except FileNotFoundError as e:
                raise Exception(f"Arquivo {filename} não encontrado") from e
        else:
            raise Exception("Tipo de argumento esperado: string")

def process(automata, word):
	words = tuple(word)

	# faz a verificação se o autônomo é um dict e se a palavra uma list
	if isinstance (automata, dict) and isinstance(word, list):
		for words in word:
			if not isinstance(words, str):
				raise Exception("necessário ser do tipo str")
	else:
		raise Exception(" ")

	try:
		alfabeto = automata['alfabeto']
		estados = automata['estados']
		estadosFinais = automata['estadosFinais']
		estadoIncial = automata['estadoIncial']
		transicoes = automata['transicoes']
	except KeyError as e:
		raise Exception(" ") from e

	# inicializa uma lista para armazenar as verificações
	verifica = []
	# aqui faz a conversão da lista de palavras em uma tupla

	# reforça sobre cada palavra na tupla de palavras
	for word in words:
		resultado = None
		# inicializa o estado atual com o estado inicial
		estadoAtual = estadoIncial
		# reforça sobre cada simbolo na palavra
		for simbolo in word:
			if resultado:
				break
		# faz a verificação se o simbolo é valido
			if simbolo not in alfabeto:
				resultado = (word, 'INVALIDA')
				verifica.append(resultado)
				break
		# itera sobre as regras de transição para encontrar a próxima transição
			for transicao in transicoes:
				if transicao[0] == estadoAtual and transicao[1] == simbolo:
					estadoAtual = transicao[2]
					break
			else:
				resultado = (word, 'REJEITA')
				verifica.append(resultado)
				break
		else:
			# Verifica se o estado atual é um estado final ou não e adiciona a resposta à lista
			if estadoAtual in estadosFinais:
				resultado = (word, 'ACEITA')
				verifica.append(resultado)
			else:
				resultado = (word, 'REJEITA')
				verifica.append(resultado)
	else:
		return verifica
