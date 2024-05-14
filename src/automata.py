"""Implementação de autômatos finitos."""
from collections import namedtuple
#import os
from typing import List
def load_automata(filename):
    #print("load_automata")
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
    Forca o commit
    """
    RegrasTransicao = namedtuple("RegrasTransicao",["origem" , "símbolo", "destino"])
    with open(filename, "rt") as arquivo:
        texto = arquivo.readlines()
        contador = 0
        automata = {
             "simbolos":[],
             "estados":[],
             "estadosFinais":[],
             "NomeEstadoInicial":"",
             "RegrasTransicao":[]
        }
        listaRegras = []
        #print(texto)
        for frase in texto:
            #print(frase)
            if contador == 0:
                simbolos = frase.split()
                automata["simbolos"].extend(simbolos)          
            elif contador == 1:
                estados = frase.split()
                automata["estados"].extend(estados)
            elif contador == 2:
                estadosFinais = frase.split()
                automata["estadosFinais"].extend(estadosFinais)
            elif contador == 3:
                NomeEstadoInicial = frase.split()
                automata.update({"NomeEstadoInicial": NomeEstadoInicial[0]})
            elif contador > 3:
                palavras = frase.split()
                if len(palavras) == 3:
                    Regras=RegrasTransicao(palavras[0],palavras[1],palavras[2])
                    #automata["RegrasTransicao"].extend(simbolos)
                    listaRegras.append(Regras)
                else :
                    try:
                        raise NameError("Regras Transisao Invalida")
                    except NameError:
                        print("Regras Transisao Invalida na sua quantidade de itens diferente de 3")
                        raise
                    break
            contador= contador + 1
            #print (contador)
        
        # processa arquivo...
      
        else:
            automata["RegrasTransicao"].extend(listaRegras)
        pass
    #print(automata)
    retStatusautomata = DescricaoautomataValida(automata)
    #words = ["ababa","cc"]
    words = ["","a","b","ab","abb","aabb","abab","baba","bbaa","abaa","bbbabaaa","bbabbaa"]
    #words = ["a","b","ab","abb","aabb","abab","baba","bbaa","abaa","bbbabaaa","bbabbbaa"]
    #retprocess = process(automata,words)
    process(automata,words)
    #print(retprocess)
def process(automata, words):
    """
    Processa a lista de palavras e retora o resultado.
    
    Os resultados válidos são ACEITA, REJEITA, INVALIDA.
    """
    caminhoDoAutonomo=""
    EstadoInicial = str(automata.get("NomeEstadoInicial"))
    estadosFinais = str(automata.get("estadosFinais"))
    simbolos = str(automata.get("simbolos"))
    listaRegras = automata.get("RegrasTransicao")
    #for regras in listaRegras:
        #print("\torigem: "+regras[0]+" símbolo: "+regras[1]+" destino: "+regras[2])
    resultado = "OK"
    DictWord={}
    for word in words:
        contador = 0;
        palavraAserMontada=""
        # tenta reconhecer `word`
        retTuple = VerificaPalavra(word,simbolos)
        if(retTuple[1]=="VALIDA"):
            if str(word)!="":
                for caractere in str(word):
                #verifica se é posição do estado inicial
                    if contador == 0:
                        for regras in listaRegras:
                            #se origem for igual estado inicial
                            if regras[0] == EstadoInicial:
                                #se simbolo for igual caracter
                                if regras[1] == caractere:
                                    caminhoDoAutonomo = caminhoDoAutonomo+ "Orig: " + regras[0] + " Simb: " + regras[1] + " Destino: " + regras[2]+ "\n"
                                    ProximaOrigem = regras[2]
                                    palavraAserMontada += caractere
                                    break
                        else:
                            ProximaOrigem=0
                            resultado="REJEITA"
                            break
                    else:
                        for regras in listaRegras:
                            #se origem for igual estado inicial
                            if regras[0] == ProximaOrigem:
                                #se simbolo for igual caracter
                                #print(regras[1] == caractere)
                                if regras[1] == caractere:
                                    caminhoDoAutonomo = caminhoDoAutonomo+ "Orig: "+ regras[0]+  " Simb: " + regras[1] + " Destino:"+regras[2] + "\n"
                                    ProximaOrigem = regras[2]
                                    palavraAserMontada += caractere
                                    break
                        else:
                            ProximaOrigem=0
                            resultado="REJEITA"
                            break
                    contador+=1
            #print(palavraAserMontada +" " + str(word))
            #print(palavraAserMontada == str(word))
            if palavraAserMontada == str(word):
                if ProximaOrigem in estadosFinais:
                    resultado = "ACEITA"
                else:
                    resultado = "REJEITA"
            else:
                resultado = "REJEITA"
            #print("\n")
            #print("CaminhoAutonomo: " + caminhoDoAutonomo)
            #print(palavraAserMontada)
            #print(resultado)    
            DictWord[word] = resultado
        else:
            if(retTuple[1]=="INVALIDA"):
                if(len(word)>0):
                    DictWord[word] = "INVALIDA"
                else:
                    if(EstadoInicial in estadosFinais):
                        DictWord[word] = "ACEITA"
            else:
                DictWord[word] = "REJEITA"
        pass
    print("Lista Palavras e resultados")
    for chave, valor in DictWord.items():
        print(f"{chave}: {valor}")
    resultado = DictWord
    #print(resultado)
    #return DictWord
#Verificar se uma palavra válida, ou seja, se todos os símbolos da palavra fazem parte do alfabeto da lingugaem
def VerificaPalavra(palavra,simbolos):
    if len(palavra)>0:
        for caractere in str(palavra):
            for simbolo in simbolos:
                if simbolo in caractere:
                    #print("SIM")
                    resultado = "VALIDA"
                    break
            else:
                #print("NAO")
                resultado = "INVALIDA"
                break
        return tuple((palavra,resultado))
    else :
        return tuple((palavra,"INVALIDA"))
def DescricaoautomataValida(automata):
    #print("DescricaoautomataValida")
    #print(automata)
    if (automata.get("simbolos")!=""
        and len(automata.get("estados"))>0
        and len(automata.get("estadosFinais"))>0
        and automata.get("NomeEstadoInicial")!=""
        and len(automata.get("RegrasTransicao"))>0):
        #verifica se os estados finais é valido com algum estado
        #verifica estados finais
        cont=0
        for esF in automata.get("estadosFinais"):
            for es in automata.get("estados"):
                if(esF == es):
                    cont+=1
                    Statusautomata="VALIDO"
                    break
        #verifica se a mesma quantidade de estados finais é valido com algum estado
        #verifica estados finais
        if(len(automata.get("estadosFinais")) == cont):
            Statusautomata="VALIDO"
        else:
            Statusautomata="INVALIDO"
            try:
                raise NameError("estadosFinais")
            except NameError:
                print("os estadosFinais Não São todos validos")
                raise
        #Zera a variavel para usar novamente no proximo teste
        Statusautomata=""
        #verifica NomeEstadoInicial
        print(automata.get("NomeEstadoInicial"))
        for es in automata.get("estados"):
            #print(es)
            #print((automata.get("NomeEstadoInicial") == es))
            if(automata.get("NomeEstadoInicial") == es):
                Statusautomata="VALIDO"
                break
            else:
                print(Statusautomata)
                if not Statusautomata == "VALIDO":
                    Statusautomata="INVALIDO"
                    try:
                        raise NameError("NomeEstadoInicial")
                    except NameError:
                        print("o Nome do Estado Inicial Não é validos")
                        raise
                    break
                    return Statusautomata
        RegrasTransicao = namedtuple("RegrasTransicao",["origem" , "símbolo", "destino"])
        regras=automata.get("RegrasTransicao")
        #print(regras)
        ListDistintaEstados = []
        ListDistintaSimbolos = []
        for r in regras:
            print(r[0]+" - " + r[1] +" - "+r[2])
            if r[0] not in ListDistintaEstados:
                ListDistintaEstados.append(r[0])
            if r[1] not in ListDistintaSimbolos:
                ListDistintaSimbolos.append(r[1])
            if r[2] not in ListDistintaEstados:
                ListDistintaEstados.append(r[2])
        #print(ListDistintaEstados)
        #print(ListDistintaSimbolos)
        #print(automata.get("simbolos"))
        cont=0
        for esL in ListDistintaEstados:
            for es in automata.get("estados"):
                if(esL in es):
                    #se existe o estado nas regras de transição e na lista de estados soma-se 1
                    cont+=1
                    Statusautomata="VALIDO"
                    break;
        #Verifica-se se para cada estado diferente em nossa regra de transisão existe um estado com mesmo nome.
        #valida a contagem se todos tiveram um correspondente
        if(len(ListDistintaEstados) == cont):
            Statusautomata="VALIDO"
        else:
            try:
                raise NameError("EstadosDaRegraTransisao")
            except NameError:
                print("Os Estados da regra de transição Nem todos São validos")
                raise
            Statusautomata="INVALIDO"
            return Statusautomata
        cont=0
        for siL in ListDistintaSimbolos:
            for si in automata.get("simbolos"):
                if(siL in si):
                    #se existe o simbolo nas regras de transição e na lista de simbolos soma-se 1
                    cont+=1
                    Statusautomata="VALIDO"
                    break;
        #Verifica-se se para cada simbolo diferente em nossa regra de transisão existe um simbolo com mesmo nome.
        #valida a contagem se todos tiveram um correspondente
        if(len(ListDistintaSimbolos) == cont):
            Statusautomata="VALIDO"
        else:
            Statusautomata="INVALIDO"
            try:
                raise NameError("SimbolosRegraTransisao")
            except NameError:
                print("O Simbolo da regra de transição Nao é valido")
                raise
            return Statusautomata
        print(Statusautomata)
        print("VALIDO")
    else:
        Statusautomata="INVALIDO"
        return Statusautomata
def convert_to_dfa(automata):
    """Converte um NFA num DFA."""
    automata["simbolos"].extend("&")
    caminhoDoAutonomo=""
    Estados = automata.get("estados"):
    EstadoInicial = str(automata.get("NomeEstadoInicial"))
    estadosFinais = str(automata.get("estadosFinais"))
    simbolos = str(automata.get("simbolos"))
    RegrasTransicao = namedtuple("RegrasTransicao",["origem" , "símbolo", "destino"])
    regras=automata.get("RegrasTransicao")
    NovaRegrasTransicao = namedtuple("RegrasTransicao",["origem" , "símbolo", "destino"])
    NovalistaRegras = []
    for(es in Estados):
        #Novo estado para unificar as transições com mesma saida
        nes = []
        for(sim in simbolos):
            for r in regras[0] == es &&
                     regras[1] == sim :
                if r[2] not in nes:
                    nes.append(r[2])                                            
            else:
                if len(nes)>1:
                    strNES= ""
                    boolEsFinal = False
                    for es in nes:
                        strNES = strNES + str(es)
                        if(es in estadosFinais)
                            boolEsFinal = True
                    NovaRegras = NovaRegrasTransicao(es,sim,strNES)
                    automata["estados"].extend(strNES)
                    if(boolEsFinal):
                        automata["estadosFinais"].extend(strNES)
                else:
                    NovaRegras = NovaRegrasTransicao(es,sim,nes) 
                NovalistaRegras.append(NovaRegras)
#"""
def main():
    #caminhoPasta = os.getcwd()
    #filename = caminhoPasta + "/Testes/01-simples.txt"
    #filename = ".\\Testes\\05-invalido.txt"
    filename = "teste.txt"
    load_automata(filename)
main()
#"""
