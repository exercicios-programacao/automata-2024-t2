"""Implementação de autômatos finitos."""
from collections import namedtuple
#import os
from typing import List
def load_automata(filename):
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
    RegrasTransicao = namedtuple("RegrasTransicao",["origem" , "simbolo", "destino"])
    with open(filename, "rt") as arquivo:
        texto = arquivo.readlines()
        contador = 0
        automata = {
             "simbolos":[],
             "estados":[],
             "estadosFinais":[],
             "NomeEstadoInicial":[],
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
    #print("autoamoamaomaoaom")
    #print(automata)
    convert_to_dfa(automata)
    #print(automata)
    ###
    #remoção temporaria para teste    
    #retStatusautomata = DescricaoautomataValida(automata)
    ###
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
    print(automata)
    #print('11111111111111111111111111')
    if (automata.get("simbolos")!=""
        and len(automata.get("estados"))>0
        and len(automata.get("estadosFinais"))>0
        and automata.get("NomeEstadoInicial")!=""
        and len(automata.get("RegrasTransicao"))>0):
        #verifica se os estados finais é valido com algum estado
        #verifica estados finais
        icont=0
        for esF in automata.get("estadosFinais"):
            for es in automata.get("estados"):
                if(esF == es):
                    icont+=1
                    Statusautomata="VALIDO"
                    break
        #verifica se a mesma quantidade de estados finais é valido com algum estado
        #verifica estados finais
        if(len(automata.get("estadosFinais")) == icont):
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
        RegrasTransicao = namedtuple("RegrasTransicao",["origem" , "simbolo", "destino"])
        regras = automata.get("RegrasTransicao")
        #print(regras)
        ListDistintaEstados = []
        ListDistintaSimbolos = []
        for r in regras:
            #print(r[0]+" - " + r[1] +" - "+r[2])
            if r[0] not in ListDistintaEstados:
                ListDistintaEstados.append(r[0])
            if r[1] not in ListDistintaSimbolos:
                ListDistintaSimbolos.append(r[1])
            if r[2] not in ListDistintaEstados:
                ListDistintaEstados.append(r[2])
        print(ListDistintaEstados)
        #print(ListDistintaSimbolos)
        #print(automata.get("simbolos"))
        icont=0
        for esL in ListDistintaEstados:
            for es in automata.get("estados"):
                if str(esL) in es:
                    #se existe o estado nas regras de transição e na lista de estados soma-se 1
                    icont+=1
                    Statusautomata="VALIDO"
                    break;
        #Verifica-se se para cada estado diferente em nossa regra de transisão existe um estado com mesmo nome.
        #valida a contagem se todos tiveram um correspondente
        if(len(ListDistintaEstados) == icont):
            Statusautomata="VALIDO"
        else:
            try:
                raise NameError("EstadosDaRegraTransisao")
            except NameError:
                #print('aaa')
                #print(ListDistintaEstados)
                print("Os Estados da regra de transição Nem todos São validos")
                raise
            Statusautomata="INVALIDO"
            return Statusautomata
        icont=0
        for siL in ListDistintaSimbolos:
            for si in automata.get("simbolos"):
                if(siL in si):
                    #se existe o simbolo nas regras de transição e na lista de simbolos soma-se 1
                    icont+=1
                    Statusautomata="VALIDO"
                    break;
        #Verifica-se se para cada simbolo diferente em nossa regra de transisão existe um simbolo com mesmo nome.
        #valida a contagem se todos tiveram um correspondente
        if(len(ListDistintaSimbolos) == icont):
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
    icontprint=0
    """Converte um NFA num DFA."""
    automata["simbolos"].extend("&")
    caminhoDoAutonomo=""
    Estados = automata.get("estados")
    EstadoInicial = automata.get("NomeEstadoInicial")
    estadosFinais = automata.get("estadosFinais")
    simbolos = automata.get("simbolos")
    RegrasTransicao = namedtuple("RegrasTransicao",["origem" , "simbolo", "destino"])
    regras = automata.get("RegrasTransicao")
    NovaRegrasTransicao = namedtuple("RegrasTransicao",["origem" , "simbolo", "destino"])
    NovalistaRegras = []
    nesNdes = []
    #icont = 0
    FlagNovoEstado = False
    qtdEstados = len(Estados)
    FlagWordVazia = False
    FlagMontaDicionarioPorSimbolo = True
    origemPorSimbolo = []
    destinoPorSimbolo = []
    DicRegrasPorSimbolo = {}
    for es in Estados:
        #icont+=1
        #Novo estado para unificar as transições com mesma saida
        nes = []
        contS = len(simbolos)
        #for indexSim,sim in enumerate(simbolos):
        for sim in simbolos:
            if sim:
                if FlagMontaDicionarioPorSimbolo:
                    DicRegrasPorSimbolo["simbolo" + str(sim)] = sim
                    DicRegrasPorSimbolo["origem" + str(sim)] = []
                    DicRegrasPorSimbolo["destino" + str(sim)] = []
            for r in regras:
                #r[0] = origem
                #r[1] = simbolo
                #r[2] = destino
                if FlagMontaDicionarioPorSimbolo:
                    if r[1] == str(sim):
                        origemPorSimbolo.append(r[0])
                        destinoPorSimbolo.append(r[2])
                if r[1]=="&":
                    FlagWordVazia = True
                #if(r[1]==sim):
                    #NovaRegras = NovaRegrasTransicao(r[0],r[1],r[2])
                    #NovalistaRegras.append(NovaRegras)
                #para o mesmo estado org. e simbolo faz uma lista de estados des.
                if r[0] == es and r[1] == str(sim):
                    if r[2] not in nes:
                        #print('destino')
                        #print(r[2])
                        nes.append(r[2])
                    if len(nes)>1:
                        #agora so presciso do simbolo o resto pego de outras variaveis
                        novaRegraApartirNES={}
                        novaRegraApartirNES.clear
                        novaRegraApartirNES.update({"origem":r[0]})
                        novaRegraApartirNES.update({"simbolo":sim})
                        novaRegraApartirNES.update({"destino":nes})
                    else:
                        novaRegraApartirNES={}
                        novaRegraApartirNES.clear
                        novaRegraApartirNES.update({"origem":r[0]})
                        novaRegraApartirNES.update({"simbolo":r[1]})
                        novaRegraApartirNES.update({"destino":r[2]})
                        #print(novaRegraApartirNES)
            else:
                #uso apenas dentro da função transferido para la
                #busca variaveis para regra do indermistico
                #simboloNovaRegra = novaRegraApartirNES.get("simbolo")
                #origemNovaRegra = novaRegraApartirNES.get("origem")
                #destinoNovaRegra = novaRegraApartirNES.get("destino")
                #
                #####
                #formar o srtnes
                ##
                ##
                #
                #
                #errooo
                ####
                strNES= ""
                for esNes in sorted(nes):
                    strNES = strNES + str(esNes)
                montaNovoEstadoInserindoRegra(nes,strNES,
                                              novaRegraApartirNES,
                                              automata,
                                              nesNdes,
                                              DicRegrasPorSimbolo,
                                              NovalistaRegras,
                                              FlagMontaDicionarioPorSimbolo,origemPorSimbolo,destinoPorSimbolo)
                #
                #
                #
                '''
                if len(nes)>1:
                    strNES= ""
                    for esNes in sorted(nes):
                        strNES = strNES + str(esNes)
                    verificaEsInicialFinal(nes,strNES,automata)
                    ###começa os problemas
                    #nesNdes[0]=(["q1","q2"],"q1q2")
                    #nesNdes = (["q1","q2"],"q1q2"),
                    #          (["q1","q2"],"q1q2")
                    
                    nesNdes.append(tuple((nes,strNES)))
                    NovaRegras = NovaRegrasTransicao(origemNovaRegra,simboloNovaRegra,strNES)
                    novaRegraApartirNES.clear
                    if NovaRegras not in NovalistaRegras:
                        NovalistaRegras.append(NovaRegras)
                        DicRegrasPorSimbolo["origem" + str(simboloNovaRegra)].extend([es])
                        DicRegrasPorSimbolo["destino" + str(simboloNovaRegra)].extend([strNES])
                        #contagem de estados
                        FlagNovoEstado = True
                        #icont+=1
                    nes = []
                else:
                    if nes != []:
                        #print('destino2')
                        #print(nes[0])
                        NovaRegras = NovaRegrasTransicao(origemNovaRegra,simboloNovaRegra,destinoNovaRegra) 
                    if NovaRegras not in NovalistaRegras:
                        NovalistaRegras.append(NovaRegras)
                        DicRegrasPorSimbolo["origem" + str(sim)].extend([es])
                        DicRegrasPorSimbolo["destino" + str(sim)].extend([nes[0]])
                    nes = []
                DicRegrasPorSimbolo["origem" + str(sim)].extend(origemPorSimbolo)
                DicRegrasPorSimbolo["destino" + str(sim)].extend(destinoPorSimbolo)
                origemPorSimbolo = []
                destinoPorSimbolo = []
                '''
                #
                #
                #
        contS=-1
        FlagMontaDicionarioPorSimbolo = False
        #print('aaa')
        #if contS == -1:
        #    break
        #print('b')
        #Apos criar os novos estados
        #arrumar origem e destino quando é simbolo de vazio
        #print(NovalistaRegras)
        if FlagWordVazia == True:
            for rnova in NovalistaRegras:
                #return
                if rnova[1] == "&":
                    print('aqui')
                    print(rnova)
                    return 
                    nes = []
                    nes.append(rnova[0])
                    nes.append(rnova[2])
                    strNVEs = str(rnova[0]) + str(rnova[2]) 
                    ret = VerificaSeqDestinoVazio(rnova,strNVEs,nes,NovalistaRegras)
                    if ret != 0:
                        NovaRegras = NovaRegrasTransicao(rnova[0],"&",ret[1])
                        if tuple((ret[0],ret[1]))not in nesNdes:
                            nesNdes.append(tuple((ret[0],ret[1])))
                            if len(listaNovosEstados)>1:
                                verificaEsInicialFinal(ret[0],ret[1],automata)
                    else:
                        NovaRegras = NovaRegrasTransicao(rnova[0],"&",strNVEs)
                        if(tuple((nes,strNES))not in nesNdes):
                            nesNdes.append(tuple((nes,strNES)))
                            verificaEsInicialFinal(nes,strNES,automata)
                            if(strNES not in automata["estados"]):
                                automata["estados"].extend(strNES)
                    if NovaRegras not in NovalistaRegras :
                        NovalistaRegras.append(NovaRegras)                
        else:
            #for novasregras1 in NovalistaRegras:
            #    print(novasregras1[0] + " -- " + novasregras1[1] + " -- " + novasregras1[2])
            #percorre a lista de tuplas
            #com lista dos nomes de estados que contem o novo estado
            # e string do nome novo estado
            #print(qtdEstados)
            #print(icont)
            #print(Estados)
            #if(icont > qtdEstados):
            if FlagNovoEstado:
                FlagNovoEstado = False
                print('cheguei aqui')
                nes = []
                #nesAux =[]
                for sim in simbolos:
                    if icontS == -1:
                        break
                    origemDoSim = DicRegrasPorSimbolo.get("origem" + str(sim))
                    destinoDoSim = DicRegrasPorSimbolo.get("destino" + str(sim))
                    for esDes in nesNdes:
                        #for iEstados,esUnificado in enumerate(esDes[0]):
                        #verificaDicRegrasPorSimbolo(
                        #tuple(lista de estados,"nome do estado")
                        #
                        #
                        nes = verificaDicRegrasPorSimbolo(tuple(esDes[0],esDes[1]),origemDoSim,destinoDoSim)
                        if len(nes)>1:
                            strNES= ""
                            for esNes in sorted(nes):
                                strNES = strNES + str(esNes)
                                novaRegraApartirNES.clear
                            novaRegraApartirNES={
                                "origem":esDes[1],
                                "simbolo":sim,
                                "destino":strNES
                            }
                            montaNovoEstadoInserindoRegra(nes,strNES,novaRegraApartirNES,automata,nesNdes,DicRegrasPorSimbolo,NovalistaRegras,FlagMontaDicionarioPorSimbolo,[],[])                          
                '''
                else:
                    for es in Estados:
                        #Novo estado para unificar as transições com mesma saida
                        nes = []
                        icontS = len(simbolos)
                        
                            
                            
                            nes = verificaDicRegrasPorSimbolo(tuple([es],es),sim,DicRegrasPorSimbolo,[])
                            #print(esDes[0])
                            #origem - esDes[0]
                            #sim - sim
                            #destino - nova[] que vira str
                            
                            
                            else:
                                if len(nes)>1:
                                    #print(r)
                                    #print(es+"--"+str(nes))
                                        #print(str(es != esDes)+" + " + "".join(nes)!= es)
                                        #print(es+"--"+sim+"--"+str(nes))
                                    #if len(nes)>len(esDes):
                                        #agora so presciso do simbolo o resto pego de outras variaveis
                                        
                                        #novaRegraApartirNES={
                                        #    "origem":es,
                                        #    "simbolo":sim,
                                        #    "destino":nes
                                        #}
                                        #garanti que a montagem do nome do estado fica na mesma ordem sempre
                                        strNES = ""
                                        #Estados = automata.get("estados")
                                        #print(Estados)
                                        #for esOrdem in Estados:
                                        for n in sorted(nes):
                                            strNES = strNES + n
                                        nes = []
                                            #if es == "q1q2":
                                            #    print(strNES)
                                        if(strNES not in automata["estados"]):
                                            automata["estados"].extend(strNES)
                                        NovaRegras = NovaRegrasTransicao(esDes[1],sim,strNES)
                                        #icontprint = icontprint + 1
                                        #print(icontprint)
                                        #print(NovaRegras)
                                        #novaRegraApartirNES.clear
                                        if NovaRegras not in NovalistaRegras:
                                            #print(NovaRegras)
                                            #print(nes)
                                            NovalistaRegras.append(NovaRegras)
                            icontS =-1              
                            #print(esSim)    
                        #print(novaRegraApartirNES)
                        #print(nesNdes)
                        #percorre lista com cada estado que esta no nome do novo estado
                        #print(esDes[0])
                        #for regras in NovalistaRegras:
                            #regras[0] == origem
                            #print('ab')
                            #print(esDes[1])
                            #novaRegraApartirNES={
                            #        "origem":"",
                            #        "simbolo":regras[1],
                            #        "destino":""
                            #}
                            #falta resolver possiveis inderterministicos criados agora com os novos estados
                            #falta arrumar(verificar e inserir) o autonomo (estados ,estados iniciais e finais)
                        #######################################
                        ### parei nessa parte de deletar o estados
                        #######################################
                        #delete dos estados originais apos unificação
                        #bkp do automato estados 
                        #atualizaEstados = automata["estados"]
                        #'''
    #print("-------------")
    #print(automata["estados"])
    regras = automata.get("RegrasTransicao")
    print("------------------")
    #print(automata["estados"])
    for novasregras in regras:
        print(novasregras[0] + " -- " + novasregras[1] + " -- " + novasregras[2])
    print("------------------")
    #print(DicRegrasPorSimbolo)
    for iSim in simbolos:
        print(DicRegrasPorSimbolo.get("simbolo"+ str(iSim)))
        print("s\n")
        print(DicRegrasPorSimbolo.get("origem"+ str(iSim)))
        print("o\n")
        print(DicRegrasPorSimbolo.get("destino" + str(iSim)))
        print("d\n")
    for novasregras1 in NovalistaRegras:
        print(str(novasregras1[0]) + " -- " + str(novasregras1[1]) + " -- " + str(novasregras1[2]))
    automata["RegrasTransicao"] = []
    automata["RegrasTransicao"] = NovalistaRegras
def montaNovoEstadoInserindoRegra(nes,strNES,novaRegraApartirNES,automata,nesNdes,DicRegrasPorSimbolo,NovalistaRegras,FlagMontaDicionarioPorSimbolo,origemPorSimbolo,destinoPorSimbolo):
    NovaRegrasTransicao = namedtuple("RegrasTransicao",["origem" , "simbolo", "destino"])
    FlagNovoEstado = False
    #print(novaRegraApartirNES)
    simboloNovaRegra = novaRegraApartirNES.get("simbolo")
    origemNovaRegra = novaRegraApartirNES.get("origem")
    destinoNovaRegra = novaRegraApartirNES.get("destino")
    if len(nes)>1:
        verificaEsInicialFinal(nes,strNES,automata)
        ###começa os problemas
        #nesNdes[0]=(["q1","q2"],"q1q2")
        #nesNdes = (["q1","q2"],"q1q2"),
        #          (["q1","q2"],"q1q2")
        nesNdes.append(tuple((nes,strNES)))

        NovaRegras = NovaRegrasTransicao(origemNovaRegra,simboloNovaRegra,strNES)
        if NovaRegras not in NovalistaRegras:
            NovalistaRegras.append(NovaRegras)
            if FlagMontaDicionarioPorSimbolo == False:
                DicRegrasPorSimbolo["origem" + str(simboloNovaRegra)].extend([origemNovaRegra])
                DicRegrasPorSimbolo["destino" + str(simboloNovaRegra)].extend([strNES])
            #contagem de estados
            FlagNovoEstado = True
            #icont+=1
        
        nes = []
    else:
        NovaRegras = NovaRegrasTransicao(origemNovaRegra,simboloNovaRegra,destinoNovaRegra) 
        if NovaRegras not in NovalistaRegras:
            NovalistaRegras.append(NovaRegras)
            DicRegrasPorSimbolo["origem" + str(simboloNovaRegra)].extend([origemNovaRegra])
            DicRegrasPorSimbolo["destino" + str(simboloNovaRegra)].extend([destinoNovaRegra])
        nes = []
        if FlagMontaDicionarioPorSimbolo:
            DicRegrasPorSimbolo["origem" + str(simboloNovaRegra)].extend(origemPorSimbolo)
            DicRegrasPorSimbolo["destino" + str(simboloNovaRegra)].extend(destinoPorSimbolo)
    origemPorSimbolo = []
    destinoPorSimbolo = []
    novaRegraApartirNES.clear
#
#Fim Do montaNovoEstadoInserindoRegra#
#
#estados unificados é uma tupla com lista de estados e nome final do estado
#para verifica estado so usar a mesma tupla estados unificados
def verificaDicRegrasPorSimbolo(estadosUnificados,orig,dest):
    nesRegrasPorSimbolo = []
    for i,o in enumerate(orig):
    #o - origem
        #if str(o) == str(estado):
        #    if dest[i] not in nes:
        #        nes.append(dest[i])
        #else:
        for esUni in estadosUnificados[0]:
            if str(o) == esUni:
                if dest[i] not in nesRegrasPorSimbolo:
                    nesRegrasPorSimbolo.append(dest[i])
                    #removido o break por poder aver inumeros destino 
                    #break
    return nesRegrasPorSimbolo
#estado == "q1q2"
    '''if estado == "q1" and sim == "a" and estadosUnificados != []:
        print(estadosUnificados)
        print("------qqq---------")
        print(nes)
        print("------qqq------")'''
    return nes
def VerificaSeqDestinoVazio(destino,strNovoEs,listaEs,listaRegras):
    VarControle = 0
    #ANTIGO NovalistaRegras
    #ANTIGO rnova
    for rSeqVazio in listaRegras:
        if(rSeqVazio[0] == destino):
            if VarControle == 0:
                if not len((rIF in rSeqVazio[1] != "&"))>0:
                    for rSeqVazio2 in rSeqVazio[1] == "&":
                        #ANTIGO NES
                        listaEs.append(rSeqVazio[2])
                        #ANTIGO strNVEs
                        strNovoEs = str(strNovoEs) + str(rSeqVazio2[2])
                        VarControle = 1
                        ret = ret+ VerificaSeqDestinoVazio(rSeqVazio2[2],strNovoEs,listaEs,listaRegras)
                        if ret != 0:
                            #print('retorno')
                            #print(ret)
                            #verificar se os retornos concatena certo as tuples ou modificar para lista de tuples
                            if ret>len(2):
                                return tuple(ret[-2],ret[-1])
                            else:
                                return tuple(listaEs,strNovoEs)
                        break
            else:
                break
    return 0
def verificaEsInicialFinal(listaNovosEstados,strEstadoNovo,automata):
    #print("listanovos estados")
    #print(listaNovosEstados)
    #print("strEstadoNovo")
    #print(strEstadoNovo)
    #print("estados")
    #print(automata["estados"])
    if len(listaNovosEstados)>1:
        boolEsFinal = False
        boolEsInicial = False
        for es in listaNovosEstados:
            if es in automata["estadosFinais"]:
                boolEsFinal = True
            if es in automata["NomeEstadoInicial"]:
                boolEsInicial = True
            if boolEsFinal and boolEsInicial:
                break
    else:
        return 0
    if boolEsFinal:
        automata["estadosFinais"].extend([strEstadoNovo])
    if boolEsInicial:
        #automata["NomeEstadoInicial"].extend(strEstadoNovo)
        automata.update({"NomeEstadoInicial": strEstadoNovo})
    if strEstadoNovo not in automata["estados"]:
        automata["estados"].extend([strEstadoNovo])
    return 0
#"""
def main():
    #caminhoPasta = os.getcwd()
    #filename = caminhoPasta + "/Testes/01-simples.txt"
    #filename = ".\\Testes\\05-invalido.txt"
    filename = "teste.txt"
    load_automata(filename)
main()
#"""
