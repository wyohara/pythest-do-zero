import pytest


# criando a fixture
@pytest.fixture
def primeiro_valor():
    return "a"


# criando a fixture
@pytest.fixture
def segundo_valor():
    return 2

# criando a fixture
@pytest.fixture
def ordenar(primeiro_valor, segundo_valor):
    return [primeiro_valor, segundo_valor]

# criando a fixture
@pytest.fixture
def lista_esperada():
    return ["a", 2, 3.0]


def test_lista_inteiro(ordenar):
    ordenar.append(3)
    assert ordenar == ["a", 2, 3]


def test_lista_mista(ordenar, lista_esperada):
    ordenar.append(3.0)
    assert ordenar == lista_esperada