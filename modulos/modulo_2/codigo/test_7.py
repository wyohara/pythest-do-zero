#!/usr/bin/env python3
import pytest
import os

#=================================================
#       Método recomendado com yield
#=================================================
# Execute o comando:
# py.test.exe .\modulos\modulo_2\codigo\test_7.py

@pytest.fixture
def verificar_arquivo_texto():
    path = "arquivo.txt"
    with open(path, "w", encoding='utf-8') as f:
        f.write('arquivo criado\n')
    yield path
    os.remove(path)


def test_1(verificar_arquivo_texto):    
    with open(verificar_arquivo_texto, "r", encoding='utf-8') as f:
        texto = f.read()
        assert 'arquivo criado' in texto


#===================================================
#       Método antigo com addfinalizer
#   É funcional, mas não é recomendado
#===================================================

@pytest.fixture
def verificar_arquivo_texto_addfinalizer(request):
    path = "arquivo.txt"
    
    with open(path, "w", encoding='utf-8') as f:
        f.write('arquivo criado\n')
    
    def excluir_arquivo_texto():
        if os.path.exists(path):
            os.remove(path)
    
    request.addfinalizer(excluir_arquivo_texto)    
    return path


def test_2(verificar_arquivo_texto_addfinalizer):    
    with open(verificar_arquivo_texto_addfinalizer, "r", encoding='utf-8') as f:
        texto = f.read()
        assert 'arquivo criado' in texto
    