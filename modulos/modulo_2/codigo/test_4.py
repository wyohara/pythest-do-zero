#!/usr/bin/env python3
import pytest

#==============================================================
#           Teste de ordem de execução de fixtures
# =============================================================

# py.test.exe .\modulos\modulo_2\codigo\test_4.py


# da primeira fixture
@pytest.fixture
def primeira_letra():
    return "a"


# usa a fixture anterior para criar a fixture ordenar
@pytest.fixture
def ordenar(primeira_letra):
    return [primeira_letra]


def testar_lista(ordenar):
    ordenar.append("b")
    assert ordenar == ["a", "b"]