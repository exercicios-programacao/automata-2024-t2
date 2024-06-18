Feature: Simular um automato finito determinístico.

Scenario: Simular um DFA mínimo.
Given a descrição de um automato finito
    """
    a
    q0
    q0
    q0
    q0 a q0
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

Scenario: Simula um DFA que verifica pares de 'a' e 'b', com no mínimo um de cada.
Given a descrição de um automato finito
    """
    a b
    q0 q1 q2 q3 q4
    q4
    q0
    q0 a q1
    q0 b q2
    q1 a q4
    q1 b q3
    q2 a q3
    q2 b q4
    q3 a q2
    q3 b q1
    q4 a q1
    q4 b q2
    """
When eu peço a validação das palavras
    """
    
    a
    b
    ab
    abb
    aabb
    abab
    baba
    bbaa
    bbbabaaa
    bbabbaa
    """
Then nenhum erro ocorre na criação do automato
    And o resultado obtido é
    """
    : REJEITA
    a: REJEITA
    b: REJEITA
    ab: REJEITA
    abb: REJEITA
    aabb: ACEITA
    abab: ACEITA
    baba: ACEITA
    bbaa: ACEITA
    bbbabaaa: ACEITA
    bbabbaa: REJEITA
    """

Scenario: Simula um DFA que aceita palavras formadas por pares de letras a e b.
Given a descrição de um automato finito
    """
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
    """
When eu peço a validação das palavras
    """
    
    a
    b
    ab
    abb
    aabb
    abab
    baba
    bbaa
    abaa
    bbbabaaa
    bbabbaa
    """
Then nenhum erro ocorre na criação do automato
    And o resultado obtido é
    """
    : ACEITA
    a: REJEITA
    b: REJEITA
    ab: ACEITA
    abb: REJEITA
    aabb: ACEITA
    abab: ACEITA
    baba: ACEITA
    bbaa: ACEITA
    abaa: ACEITA
    bbbabaaa: ACEITA
    bbabbaa: REJEITA
    """


# Scenario: Simula um DFA 
# Given a descrição de um automato finito
# When eu peço a validação das palavras
# Then nenhum erro ocorre na criação do automato
#     And o resultado obtido é
