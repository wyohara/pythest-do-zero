#!/usr/bin/env python3
import pytest

#=================================================
#       Testando fixtures automáticas
#=================================================
# Execute o comando:
# py.test.exe .\modulos\modulo_2\codigo\test_6.py

@pytest.fixture
def primeira_entrada():
    return "a"


@pytest.fixture
def lista_ordenada(primeira_entrada):
    return []


#fixture de uso automático
@pytest.fixture(autouse=True)
def append_first(lista_ordenada, primeira_entrada):
    #irá adicionar o valor 'a' a lista automaticamente
    return lista_ordenada.append(primeira_entrada)


def test_somente_String(lista_ordenada, primeira_entrada):
    #verifica se a fixture automática funcionou, logo ['a']==['a']
    assert lista_ordenada == [primeira_entrada]


def test_string_and_int(lista_ordenada, primeira_entrada):
    #verifica se a fixture tornou ['a',2]
    lista_ordenada.append(2)
    assert lista_ordenada == [primeira_entrada, 2]