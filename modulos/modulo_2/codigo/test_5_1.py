#!/usr/bin/env python3

import pytest

#==============================================================
#           Teste de ordem de execução de fixtures
# =============================================================

# py.test.exe -s .\modulos\modulo_2\codigo\test_5_1.py
# O -s exibe os prints

@pytest.fixture
def fixture_yield1():
    yield
    print("Executado o yield 1")


@pytest.fixture
def fixture_yield2():
    yield
    print("Executado o yield 2")


def test_ordem_fixture(fixture_yield1, fixture_yield2):
    print("test_bar")

