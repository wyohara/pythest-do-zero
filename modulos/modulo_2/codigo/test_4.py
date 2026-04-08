import pytest


# Preparo com a fixture
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