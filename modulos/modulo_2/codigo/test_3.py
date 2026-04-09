#!/usr/bin/env python3
import pytest

#==============================================================
#           Uso repetitivo de fixtures
# =============================================================

# py.test.exe .\modulos\modulo_2\codigo\test_3.py

class Fruta:
    'Classe que define se a fruta foi corada ou não'
    def __init__(self, nome):
        self.nome = nome
        self.cortado = False

    def cortar(self):
        self.cortado = True

class SaladaDeFruta:
    'Classe que cria a salada de frutas usando a classe Frutas'
    def __init__(self, *tigela_de_frutas):
        # o asterisco é usado para desempacotar a lista usando um por vez
        self.fruta = tigela_de_frutas
        self._cortar_frutas()

    def _cortar_frutas(self):
        for fruta in self.fruta:
            fruta.cortar()

# Preparo com a fixture
@pytest.fixture
def tigela_de_frutas():
    return [Fruta("maçã"), Fruta("banana")]

#teste usando a fixture
def test_salada_de_fruta(tigela_de_frutas):
    salada_de_fruta = SaladaDeFruta(*tigela_de_frutas)

    #verifica todos as frutas da tigela de frutas
    assert all(fruta.cortado for fruta in salada_de_fruta.fruta)