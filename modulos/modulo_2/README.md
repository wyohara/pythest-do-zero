# Um mergulho no pytest

## Execução de testes   

O pytest permite executar o teste através do comando `py.test.exe .\test_1.py` porém também podemos executar todos os testes executando `py.test.exe`. Nesse caso ele irá procurar no código fonte todos os arquivos test_*.py e executar.  
Outra opção é executar.  

Opcionamente podemos rodar uma função de teste específica usando `::`:
```python
#executando o teste test_quadrado
py.test.exe -q .\test_1.py::test_quadrado

#para executar o teste que falha
py.test.exe -q .\test_1.py::test_quadrado_falha
```

No caso de uma classe podemos executar separadamente
```python
#executando a classe de teste inteira
py.test.exe -q .\test_1.py:::TestQuadrado   

#para executar a função test_quadrado da classe TestQuadrado
py.test.exe -q .\test_1.py::TestQuadrado::test_quadrado
```  
O codigo pode ser conferido [aqui](/modulos/modulo_2/codigo/test_1.py)  

---
## Verificando testes com assert
O pytest usa a função padrão `assert` do python para verificar se o teste funciona corretamente.
```python
def quadrado(x):
    return x **2

def test_quadrado():
    assert quadrado(2) == 4
```  
O codigo pode ser conferido [aqui](/modulos/modulo_2/codigo/test_1.py)  

Quando usamos **ponto flutuante** o assert pode  ter erro de aproximação, então usamos `pytest.approx()`.  

```python
import pytest

def test_floats():
    assert (0.1 + 0.2) == pytest.approx(0.3)
```  
O codigo pode ser conferido [aqui](/modulos/modulo_2/codigo/test_1.py)

---
### Verificando excessões
Quando queremos verificar exceções podemos amarrar com `with pytest.raises()`.  

```python
import pytest


def test_zero_division():
    with pytest.raises(ZeroDivisionError):
        1 / 0
```  
O codigo pode ser conferido [aqui](/modulos/modulo_2/codigo/test_2.py)

Se capturarmos o erro durante a execução podemos tratar com pytest para saber qual o problema em específico o código tem:

```python
def test_recursion_depth():
    with pytest.raises(RuntimeError) as excessao:

        def recursao(): #cria a função
            recursao() # cria uma recursão infinita

        recursao() # excuta a função

    # captura a excessão e confirma se ela foi de 'maximum recursion'
    assert "maximum recursion" in str(excessao.value)
```  
O codigo pode ser conferido [aqui](/modulos/modulo_2/codigo/test_2.py)


Para capturar exceções personalizadas podemos usar [expressões regulares](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Regular_expressions) para capturar mensagens de erro:

```python
import pytest


def excessao_personalizada():
    raise ValueError("Exception 123 lançada")


def test_mensagem_erro():
    with pytest.raises(ValueError, match=r".* 123 .*"):
        excessao_personalizada()
```  
O codigo pode ser conferido [aqui](/modulos/modulo_2/codigo/test_2.py)


Além de capturar o erro podemos capturar erros com base na hierarquia, pois o python estabelece hierarquia entre os tipos de erros. A lista de hierarquia está [aqui](https://docs.python.org/3/library/exceptions.html#exception-hierarchy).  
Veja o exemplo:

```python
import pytest

def test_excessao_grupo():
    with pytest.RaisesGroup(ValueError):
        raise ExceptionGroup("grupo da mensagem", [ValueError("valor da mensagem")])
```  
O codigo pode ser conferido [aqui](/modulos/modulo_2/codigo/test_2.py)


#### Marcando bugs com xfail
Caso exista um trecho de código com bug ou problema podemos marcar com `xfail`, um decorator que diz ao teste que esperamos uma falha programada, assim o teste é tratado como sucesso quando executado.

```python
import pytest
def codigo_bugado():
    raise IndexError() # ele lança um Index error


@pytest.mark.xfail(raises=IndexError, , reason="Bug conhecido no código")
def test_codigo_bugado(): #criamos um teste onde esperamos um IndexError
    codigo_bugado()
```  
O codigo pode ser conferido [aqui](/modulos/modulo_2/codigo/test_2.py)


#### Diferença do raise para xfail
O `raise` representa um teste onde esperamos que ocorra um erro naturalmente. Por exemplo se o requisito for permitir somente a insersão de uma string lida no banco de dados, podemos lançar um erro se o texto estiver vazio. Assim criamos um teste onde testamos se inserir um testo vazio ocorre erro e esperamos que isso aconteça.
    *O raise exception é muito útil para para cobrir um dos princícios do python: 'melhor pedir desculpas que por favor'.  
    Ou seja, é melhor amarrar com try/except e tratar o erro do que amarrar uma cadeia de if/elif/else para tratar todas as possibilidades.*  

Já o `xfail` é útil para tratar um bug ou **problema que sabemos que existe, mas não conseguimos resolver**. Quando o bug for resolvido - ou criamos um novo bug - ***o xfail irá lançar erro, permitindo rastrear o problema***.  

---
## Entendendo as fixtures  

Fixutes são cenários preparados para rodar os testes. É por meio das fixtures que evitamos códigos repetitivos. Veja um exemplo abaixo:

```python
import pytest

class Fruta:
    def __init__(self, nome):
        self.nome = nome
        self.cortado = False

    def cortar(self):
        self.cortado = True

class SaladaDeFruta:
    def __init__(self, *tigela_de_frutas):
        # o asterisco é usado para desempacotar a lista usando um por vez
        self.fruta = tigela_de_frutas
        self._cortar_frutas()

    def _cortar_frutas(self):
        for fruta in self.fruta:
            fruta.cortar()

# Preparo com a fixture
@pytest.fixture
def tigela_de_frutas():
    return [Fruta("maçã"), Fruta("banana")]

#teste usando a fixture
def test_salada_de_fruta(tigela_de_frutas):
    salada_de_fruta = SaladaDeFruta(*tigela_de_frutas)

    #verifica todos as frutas da tigela de frutas
    assert all(fruta.cortado for fruta in salada_de_fruta.fruta)
```  
O codigo pode ser conferido [aqui](/modulos/modulo_2/codigo/test_3.py)  


Uma fixture também pode ser usada em cadeia, combinando com outras fixtures. Mas cuidado, ***a necessidade de usar muitas fixutes em cadeia ou muito longas, significa que o seu código está muito acoplado, sendo necessário refatorar.***  

```python
import pytest


# Preparo com a fixture
@pytest.fixture
def primeira_letra():
    return "a"


# usa a fixture anterior para criar a fixture ordenar
@pytest.fixture
def ordenar(primeiro_valor):
    return [primeiro_valor]


def testar_lista(ordenar):
    ordenar.append("b")
    assert ordenar == ["a", "b"]
```  
- O codigo pode ser conferido [aqui](/modulos/modulo_2/codigo/test_4.py)  


Fixtures também podem ser usadas mais de uma vez nos testes. As fixtures também podem ser usadas por mais de um teste.

```python
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
```
- O codigo pode ser conferido [aqui](/modulos/modulo_2/codigo/test_5.py)  
