#!/usr/bin/env python3

#==============================================================
#      Arquivo de teste de escopo de arquivo, modulo e sessão
# =============================================================
# py.test.exe .\modulos\modulo_2\codigo\teste_escopo



def test_1_1(fixture_escopo_modulo, fixture_escopo_pacote, fixture_escopo_session):
    #sempre que iniciar o teste irá ocorrer somente uma ativação do escopo de sessão logo só ['sessao_criada']
    assert fixture_escopo_session == ['sessao_criada']
    #sempre que iniciar o teste irá ocorrer somente uma ativação do escopo de pacote para cada pasta e subpasta, logo ['pacote_criado']
    assert fixture_escopo_pacote == ['pacote_criado']
    #a cada arquivo será criado um escopo de módulo, logo neste primeiro teste será ['modulo_criado']
    assert fixture_escopo_modulo == ['modulo_criado']


def test_1_2(fixture_escopo_modulo,fixture_escopo_pacote, fixture_escopo_session):
    assert fixture_escopo_session == ['sessao_criada']
    assert fixture_escopo_pacote == ['pacote_criado']
    assert fixture_escopo_modulo == ['modulo_criado']