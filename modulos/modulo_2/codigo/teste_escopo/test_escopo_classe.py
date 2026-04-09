#!/usr/bin/env python3
import pytest


#==============================================================
#           Arquivo de teste de escopo de classe
# =============================================================
# py.test.exe .\modulos\modulo_2\codigo\teste_escopo

contador = []
@pytest.fixture(scope="class")
def fixture_escopo_classe():
    global contador
    #incrementa o contador
    contador.append('criado')
    return contador

class TestClasseA():
    '''
    Como a fixture é de classe ao iniciar a classe ela é criada,
    fazendo com que seja ['criado']
    '''
    def test_1(self, fixture_escopo_classe):
        assert fixture_escopo_classe ==['criado']
    
    def test_2(self, fixture_escopo_classe):
        assert fixture_escopo_classe ==['criado']
    
    def test_3(self, fixture_escopo_classe):
        assert fixture_escopo_classe ==['criado']


class TestClasseB():
    '''
    Ao rodar a fixture na nova classe ela é recriada,'
    o que incrementa o contador para ['criado', 'criado']
    '''
    def test_1(self, fixture_escopo_classe):
        assert fixture_escopo_classe ==['criado', 'criado']
    
    def test_2(self, fixture_escopo_classe):
        assert fixture_escopo_classe ==['criado', 'criado']