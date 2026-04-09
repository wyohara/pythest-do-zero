#!/usr/bin/env python3

import pytest

#=================================================
#       Reaproveitamento de fixtures
#=================================================
# Execute o comando:
# py.test.exe .\modulos\modulo_2\codigo\test_5.py

@pytest.fixture
def primeiro_valor():
    return "a"


@pytest.fixture
def segundo_valor():
    return 2


#fixture que usa os dados de primeiro_valor() e segundo_valor()
@pytest.fixture
def ordenar(primeiro_valor, segundo_valor):
    return [primeiro_valor, segundo_valor]

#fixture para comparar os resultados
@pytest.fixture
def lista_mista_esperada():
    return ["a", 2, 3.0]


def test_lista_inteiro(ordenar):
    ordenar.append(3)
    assert ordenar == ["a", 2, 3]


def test_lista_mista(ordenar, lista_mista_esperada):
    ordenar.append(3.0)
    assert ordenar == lista_mista_esperada