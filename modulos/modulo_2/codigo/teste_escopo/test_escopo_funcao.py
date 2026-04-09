#!/usr/bin/env python3
import pytest


#==============================================================
#           Arquivo de teste de escopo de função
# =============================================================
# py.test.exe .\modulos\modulo_2\codigo\teste_escopo

contador = []
@pytest.fixture(scope="function")
def fixture_escopo_funcao():
    global contador
    #incrementa o contador
    contador.append("criado")
    return contador

def test_1(fixture_escopo_funcao):
    # por ser escopo função ao fim da função a fixture é destruida
    # a variavel global ao criar a fixture adiciona ao array 'criado'
    assert fixture_escopo_funcao == ['criado']
        
def test_2(fixture_escopo_funcao):
    # por ser escopo função ao fim da função a fixture é destruida
    # a variavel global ao criar a fixture adiciona ao array 'criado'
    assert fixture_escopo_funcao == ['criado','criado']

def test_3(fixture_escopo_funcao):
    # por ser escopo função ao fim da função a fixture é destruida
    # a variavel global ao criar a fixture adiciona ao array 'criado'
    assert fixture_escopo_funcao == ['criado','criado', 'criado']