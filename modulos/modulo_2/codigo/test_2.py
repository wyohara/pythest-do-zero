import pytest

def ponto_flutuante():
    return 0.2 + 0.1

def divisao_zero():
    return 1 / 0

def recursao():  # cria a função
    return recursao()  # cria uma recursão infinita

def excessao_personalizada():
    raise ValueError("Exception 123 lançada")

def codigo_bugado():
    raise IndexError #lança um Index error



class TestExceptions():
    def test_ponto_flutuante(self):
        assert ponto_flutuante() == pytest.approx(0.3)
    
    def test_divisao_excessao(self):
        with pytest.raises(ZeroDivisionError):
            divisao_zero()
    
    def test_recursao_excessao(self):
        with pytest.raises(RecursionError) as ex:
            recursao()
            # captura a exceção e confirma se ela foi de 'maximum recursion'
        assert "maximum recursion" in str(ex.value)
    
    def test_excessao_personalizada(self):
        with pytest.raises(ValueError, match=r".* 123 .*"):
            excessao_personalizada()
    
    def test_excessao_grupo(self):
        with pytest.RaisesGroup(ValueError):
            raise ExceptionGroup("grupo da mensagem", [ValueError("valor da mensagem")])
        
    @pytest.mark.xfail(raises=IndexError,  reason="Bug conhecido no código")
    def test_codigo_bugado(self): #criamos um teste onde esperamos um IndexError
        codigo_bugado()