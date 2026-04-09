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


Uma fixture também pode ser usada em cadeia, combinando com outras fixtures.  
    Mas cuidado!  
A necessidade de usar muitas fixutes em cadeia ou muito longas, significa que o ***seu código está muito acoplado, sendo necessário refatorar.***  

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

Além disso as fixtures sempre ***são executadas da direita para a esquerda***:  
*OBS: pode usar -s para mostrar os prints.*
```python

```

---
## fixtures automáticas

Outra grande vantagem das fixtures é sua capacidade de se adaptar aos testes de forma simples e intuitiva. Entendendo o básico das fixtures vamos começar a olhar os comandos avançados das fixtures.  

As fixtures não precisam ser chamadas diretamente, você pode definir fixtures que são executadas automaticamente em cada teste:  
```python
import pytest


@pytest.fixture
def primeira_entrada():
    return "a"


@pytest.fixture
def lista_ordenada(primeira_entrada):
    return []


#fixture de uso automático
@pytest.fixture(autouse=True)
def append_first(lista_ordenada, primeira_entrada):
    #irá adicionar o valor 'a' a lista automaticamente
    return lista_ordenada.append(primeira_entrada)


def test_somente_String(lista_ordenada, primeira_entrada):
    #verifica se a fixture automática funcionou, logo ['a']==['a']
    assert lista_ordenada == [primeira_entrada]


def test_string_and_int(lista_ordenada, primeira_entrada):
    #verifica se a fixture tornou ['a',2]
    lista_ordenada.append(2)
    assert lista_ordenada == [primeira_entrada, 2]
```  
- O codigo pode ser conferido [aqui](/modulos/modulo_2/codigo/test_6.py)  


---
## fixture por escopo  

Mas e se eu quiser usar uma fixture em outro local fora do arquivo, como proceder? para isso usamos o ***scope***. Ele altera o escopo de trabalho da fixture podendo ser usado em vários níveis:  
1. `scope='function'` - é o escopo padrão. A fixture é destruída ao fim da execução de cada ***função ou método***.
2. `scope='class'` - éo escopo de classe. A fixture é destruída ao fim da execução da **classe de teste**.
3. `scope='module'` - o escopo de módulo ou arquivo. A fixture só é destruída ao fim da execução do **arquivo de testes**, tendo um ou vários testes.
4. `scope='package'` - o escopo de pacote ou pasta, que é composto por um ou vários arquivos. A fixture só é destruída ao fim da execução dos **testes na pasta**.
5. `scope='session'` - o escopo de sessão de testes, podendo conter vários pacotes. A fixture só é encerrada ao fim da **dos testes**.
6. `scope='determine_scope'` - o pytest determina por ta própria o tipo de scope
- É o brigatório que a fixture que opere em escopo separado fique no arquivo `contest.py`.  
- Vale destacar que cada fixture só possui uma instância, assim se criar uma fixtura com mesmo nome, ela será reescrita.  
- O código pode ser verificado [aqui](/modulos/modulo_2/codigo/teste_escopo/) 

### Uso de fixture sem repetição
Quando for usar fixtures muito repetitivas, podemos usar o escopo para manter as configurações fixas. Normalmente usamos `scope='class' autouse=True`:

```python
@pytest.fixture(scope="class")
def landing_page(driver, login):
    """Página inicial - depende do login que já aconteceu."""
    return LandingPage(driver)

class TestPaginaInicialSuccesso:
    @pytest.fixture(scope="class", autouse=True)
    def login(self, driver, url, user):
        "Esse setup executado UMA vez para toda a classe. Assim podemos usar os métodos para os testes."
        driver.get(urljoin(url, "/login"))
        pagina = LoginPage(driver)
        pagina.login(user)
    
    def test_nome_no_header(self, landing_page, user):
        #landing_page seria fixture que retorna a tela
        assert landing_page.header == f"Welcome, {user.name}!"
    
    def test_sign_out_button(self, landing_page):
        #landing_page seria fixture que retorna a tela
        assert landing_page.sign_out_button.is_displayed()
    
    def test_profile_link(self, landing_page, user):
        #landing_page seria fixture que retorna a tela
        assert landing_page.profile_link.get_attribute("href") == profile_href
```

---
## Ciclo de vida da fixture

Teardown é o processo de desmontar a fixture após terminar o seu uso, ela serve para funções como:
- Remover dados criados durante o teste
- Fechar conexões (banco, rede, arquivos)
- Restaurar o sistema ao estado original

Para isso usamos o comando `yield` [aqui](https://docs.python.org/pt-br/3/reference/expressions.html#yield-expressions) onde lançamos os valores e pausamos a fixture e esperamos o teste ser concluido para terminar a fixuture:
1. Criamos a fixture
2. Montamos todos os valores necessário. Ex.: abrir consulta com o banco
3. Entregamos o dados com yield
4. Aguardamos o teste acabar
5. Desmontamos os dados. Ex.: fechar consulta com o banco
6. Encerramos a fixture

veja o exemplo:
```python
import pytest
import os

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
```  
- O código pode ser verificado [aqui](/modulos/modulo_2/codigo/test_7.py)  

É possível desmontar o código usando `request.addfinalizer` que agenda a exclusão do teste após a conclusão, mas lembre-se que o o processo de desmonte do teste respeita o [scope](#fixture-por-escopo).  

``` python
@pytest.fixture
def criar_arquivo_texto(request):
    path = "arquivo.txt"
    
    with open(path, "w", encoding='utf-8') as f:
        f.write('arquivo criado\n')
    
    def excluir_arquivo_texto():
        if os.path.exists(path):
            os.remove(path)
    
    request.addfinalizer(excluir_arquivo_texto)
    
    return path

def test_2(criar_arquivo_texto):    
    with open(criar_arquivo_texto, "r", encoding='utf-8') as f:
        texto = f.read()
        assert 'arquivo criado' in texto    
```  
- O código pode ser verificado [aqui](/modulos/modulo_2/codigo/test_7.py)  

## Uso seguro do teardown
Durante o processo de desmonte do teste ou ***teardown*** é preciso tomar alguns cuidados para que não ocorra risco no desmonte. Para demonstrar image o cenário hipotético:  

```python

@pytest.fixture
def setup_problematico():    
    servidor_1 = TCPServer(8888)
    servidor_2 = TCPServer(8889)
    servidor_1.start()
    servidor_2.start()
    
    # Envia mensagem do servidor_1 para o servidor_2
    message = "Olá, servidor 2!"
    servidor_1.enviar_mensagem(message, servidor_2)
    time.sleep(0.1)
    
    yield servidor_2, message

    #============================================================
    # Teardown - PODE NÃO EXECUTAR se houver erro nas mensagens
    servidor_2.limpar_mensagens()
    servidor_1.stop()
    servidor_2.stop()


def test_mensagem_problematica(setup_problematico):
    server2, message = setup_problematico
    assert message in server2.mensagens
    print(f"[TESTE] Mensagem recebida: {server2.mensagens}")
```  
- O código pode ser verificado [aqui](/modulos/modulo_2/codigo/test_8.py)  

Exemplo de uma fixture com problemas:
```python
#==========================================
#       Setup com defeito forçado
#==========================================
@pytest.fixture
def setup_com_erro():
    "Fixture que falha no meio do setup."
    
    server1 = TCPServer(8888)
    server2 = TCPServer(8889)
    server1.start()
    server2.start()
    
    # ERRO SIMULADO AQUI!
    raise Exception("Falha crítica no setup do servidor!")
    
    # O código abaixo NUNCA executa
    message = "Esta mensagem nunca será enviada"
    server1.enviar_mensagem(message, server2)
    
    yield server2, message
    
    # TEARDOWN nunca executa!
    server2.limpar_mensagens()
    server1.stop()
    server2.stop()


def test_com_erro(setup_com_erro):
    """Este teste nunca executa devido ao erro no setup."""
    server2, message = setup_com_erro
    assert message in server2.messages
```  
- O código pode ser verificado [aqui](/modulos/modulo_2/codigo/test_8.py)  

Assim a melhor forma de executar o teardown é usar fixtures atômicas, onde cada etapa possui uma fixture. Assim não ocorre problemas na execução e no caso de falha as fixtures posteriores não serão chamadas evitando erro no teardown.  

```python
# =============================================
#       VERSÃO CORRETA (Fixtures atomicas)
# =============================================
@pytest.fixture
def server1():
    "Fixture 1: Cria o primeiro servidor."
    server = TCPServer(8888)
    server.start()
    yield server

    #teardown
    server.stop()


@pytest.fixture
def server2():
    "Fixture 2: Cria o segundo servidor."
    server = TCPServer(8889)
    server.start()
    yield server

    #teardown
    server.limpar_mensagens()
    server.stop()


@pytest.fixture
def mensagem(server1, server2):
    "Fixture 3: Enviando mensagem entre servidores."
    message = "Olá, servidor 2! Esta é uma mensagem de teste."
    server1.enviar_mensagem(message, server2)
    time.sleep(0.1)
    return message


def test_mensagem_segura(server2, mensagem):
    "Teste verificando se o servidor recebeu a mensagem"
    assert server2.verifica_mensagens(mensagem)
```  
- O código pode ser verificado [aqui](/modulos/modulo_2/codigo/test_8.py)  

### Request e introspecção
