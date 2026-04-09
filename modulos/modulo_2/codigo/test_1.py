#!/usr/bin/env python3

#==============================================================
#           Usando assert
# =============================================================
# py.test.exe .\modulos\modulo_2\codigo\test_1.py

def quadrado(x):
    # função que calcula quadrado sendo testada
    return x **2

def test_quadrado():
    #teste que é sucesso
    assert quadrado(2) == 4

def test_quadrado_falha():
    #teste que falha
    assert quadrado(3) == 5

class TestQuadrado():
    'Classe para realizar os testes'
    def test_quadrado(self):
        #teste que é sucesso na classe
        assert quadrado(2) == 4

    def test_quadrado_erro(self):
        #teste que é sucesso na classe
        assert quadrado(3) == 2
        


