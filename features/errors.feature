Feature: Não permite que erros afetem a execução do programa.

Scenario: Estados finais não estão presentes no conjunto de estados.
Given a descrição de um automato finito
    """
    a b
    q0 q1 q2
    q0 q3
    q0
    q0 a q1
    q1 b q2
    """
When eu crio o automato
Then um erro ocorre na criação do automato

Scenario: Estados inicial não está presente no conjunto de estados.
Given a descrição de um automato finito
    """
    a b
    q0 q1 q2
    q0
    q3
    q0 a q1
    q1 b q2
    """
When eu crio o automato
Then um erro ocorre na criação do automato

Scenario: Transição leva a estado que não está no conjunto de estados.
Given a descrição de um automato finito
    """
    a b
    q0 q1 q2
    q0
    q2
    q0 a q3
    q1 b q2
    """
When eu crio o automato
Then um erro ocorre na criação do automato

Scenario: Transição parte de estado que não está no conjunto de estados.
Given a descrição de um automato finito
    """
    a b
    q0 q1 q2
    q0
    q2
    q3 a q1
    q1 b q2
    """
When eu crio o automato
Then um erro ocorre na criação do automato

Scenario: Transição utiliza símbolo inválido
Given a descrição de um automato finito
    """
    a b
    q0 q1 q2
    q0
    q2
    q0 c q1
    q1 b q2
    """
When eu crio o automato
Then um erro ocorre na criação do automato

