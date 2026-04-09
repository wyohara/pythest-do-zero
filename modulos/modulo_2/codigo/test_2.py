#!/usr/bin/env python3
import pytest

#==============================================================
#           Usando assert em casos especiais
# =============================================================
# py.test.exe .\modulos\modulo_2\codigo\test_2.py

# realizando operação com ponto flutuante
def ponto_flutuante():
    return 0.2 + 0.1

# erro por divisão com zero
def divisao_zero():
    return 1 / 0

# recursão infinita
def recursao():
    return recursao()

# criando erro personalizado
def excessao_personalizada():
    raise ValueError("Exception 123 lançada")

# função com defeito lançando erro
def codigo_bugado():
    raise IndexError #lança um Index error


class TestExceptions():
    # classe para testar todos os casos
    def test_ponto_flutuante(self):
        #usando aproximação para ponto flutuante
        assert ponto_flutuante() == pytest.approx(0.3)
    
    def test_divisao_excessao(self):
        # capturando e verificando erro da divisão por zero
        with pytest.raises(ZeroDivisionError):
            divisao_zero()
    
    def test_recursao_excessao(self):
        # capturando o erro de recursão e verificando se foi erro de recursão
        with pytest.raises(RecursionError) as ex:
            recursao()
        # captura a exceção e confirma se ela foi de 'maximum recursion'
        assert "maximum recursion" in str(ex.value)
    
    def test_excessao_personalizada(self):
        # capturando erro personalizado e verificando se foi ele que ocorreu
        with pytest.raises(ValueError, match=r".* 123 .*"):
            excessao_personalizada()
    
    def test_excessao_grupo(self): 
        # Capturando excessão por grupo de famílias de erro
        # documentação: https://docs.python.org/3/library/exceptions.html#exception-hierarchy
        with pytest.RaisesGroup(ValueError):
            raise ExceptionGroup("grupo da mensagem", [ValueError("valor da mensagem")])
        
    @pytest.mark.xfail(raises=IndexError,  reason="Bug conhecido no código")
    def test_codigo_bugado(self):
        #criamos um teste onde esperamos um IndexError por bug
        # OBS quando for corrigido esse bug IRÁ SER LANÇADO O ERRO NO XFAIL
        codigo_bugado()