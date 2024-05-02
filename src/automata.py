def load_automata(filename: str):
	try:
		with open(filename, encoding="utf-8") as arquivo:
			linhas = arquivo.readlines()
			
			transicoes = {}

			if len(linhas) < 5:
				raise ValueError("Arquivo não contém suficientes linhas para representar um autômato")

			alfabeto = linhas[0].strip().split(" ")
			estados = linhas[1].strip().split(" ")
			estadosFinais = linhas[2].strip().split(" ")
			estadoIncial = linhas[3].strip(" ")

			for linha in linhas[4:]:
				transicao = linha.strip().split(" ")

				if len(transicao) < 3 or transicao[0] not in estados or transicao[1] not in alfabeto or transicao[2] not in estados:
					raise ValueError("Transição não determinística não encontrada")
				print(f"{transicao} é o correto.")

			return alfabeto, estados, estadosFinais, estadoIncial, transicoes

	except FileNotFoundError as e:
		raise ValueError(f"Arquivo {filename} não encontrado") from e


def process(automata, word):
	alfabeto, estados, estadosFinais, estadoIncial, transicoes = automata

	verifica = []
	try:
		for words in word:
			palavra = tuple(words)

			for simbolo in palavra:
				if simbolo not in alfabeto:
					verifica[words] = "INVÁLIDA"
					break
			else:
				estadoAtual = estadoIncial
				for simbolo in palavra:
					if simbolo in transicoes.get[estadoAtual, []]:
						estadoAtual = transicoes[estadoAtual][simbolo]
					else:
						verifica[words] = "REJEITA"
						break
				else:
					if estadoAtual in estadosFinais:
						verifica[words] = "ACEITA"
					else:
						verifica[words] = "REJEITA"
	except Exception as e:
		raise ValueError(f"Erro ao processar palavra {word}: {e}") from e
		
	return verifica
