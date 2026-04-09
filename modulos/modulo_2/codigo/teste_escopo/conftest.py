#!/usr/bin/env python3
import pytest


#==============================================================
#           Arquivo de configuração de testes
# =============================================================
# py.test.exe .\modulos\modulo_2\codigo\teste_escopo


contador_modulo = []
#criando a fixture que ocorre somente a nível de módulo
@pytest.fixture(scope="module")
def fixture_escopo_modulo():
    global contador_modulo
    #incrementa o contador
    contador_modulo.append('modulo_criado')
    return contador_modulo

contador_pacote = []
@pytest.fixture(scope="package")
#criando a fixture que ocorre somente a nível de pacote
def fixture_escopo_pacote():
    global contador_pacote
    #incrementa o contador
    contador_pacote.append('pacote_criado')
    return contador_pacote

contador_sessao = []
@pytest.fixture(scope="session")
#criando a fixture que ocorre somente a nível de sessão
def fixture_escopo_session():
    global contador_sessao
    #incrementa o contador
    contador_sessao.append('sessao_criada')
    return contador_sessao



