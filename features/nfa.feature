Feature: Simular um automato finito determinístico.

Scenario: Converter um NFA simples.
Given a descrição de um automato finito
    """
    a
    q0 q1
    q0
    q0
    q0 a q0
    q0 a q1
    q1 a q0
    """
When eu peço a validação das palavras
    """
    
    a
    aaaa
    aaa
    aab
    aaaaaaaa
    """
Then nenhum erro ocorre na criação do automato
    And o resultado obtido é
    """
    :ACEITA
    a:ACEITA
    aaaa:ACEITA
    aaa:ACEITA
    aab:INVALIDA
    aaaaaaaa:ACEITA
    """

Scenario: Converter um NFA com palavra vazia.
Given a descrição de um automato finito
    """
    a b
    q0 q1 q2 q3 q4 q5 q6
    q3 q6
    q0
    q0 a q1
    q0 a q4
    q1 b q2
    q2 a q3
    q4 a q5
    q5 b q6
    """
When eu peço a validação das palavras
    """
    
    a
    b
    aa
    ab
    ba
    bb
    aaa
    aab
    aba
    abb
    baa
    bab
    bba
    """
Then nenhum erro ocorre na criação do automato
    And o resultado obtido é
    """
    : REJEITA
    a: REJEITA
    b: REJEITA
    aa: REJEITA
    ab: REJEITA
    ba: REJEITA
    bb: REJEITA
    aaa: REJEITA
    aab: ACEITA
    aba: ACEITA
    abb: REJEITA
    baa: REJEITA
    bab: REJEITA
    bba: REJEITA
    """

Scenario: Converter um NFA com palavra vazia.
Given a descrição de um automato finito
    """
    a b
    q0 q1 q2 q3 q4
    q4
    q0
    q0 a q0
    q0 b q0
    q0 & q1
    q1 a q2
    q2 b q3
    q3 a q4
    """
When eu peço a validação das palavras
    """
    
    a
    aa
    ba
    aab
    aba
    aaba
    ababa
    bbaba
    aaaabbbbaba
    """
Then nenhum erro ocorre na criação do automato
    And o resultado obtido é
    """
    :REJEITA
    a:REJEITA
    aa:REJEITA
    ba:REJEITA
    aab:REJEITA
    aba:ACEITA
    aaba:ACEITA
    ababa:ACEITA
    bbaba:ACEITA
    aaaabbbbaba:ACEITA
    """

# Scenario: Simula um DFA 
# Given a descrição de um automato finito
# When eu peço a validação das palavras
# Then nenhum erro ocorre na criação do automato
#     And o resultado obtido é
