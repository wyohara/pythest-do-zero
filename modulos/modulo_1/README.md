# Módulo 1

## Entendendo o TDD

Desenvolvimento guiado por testes é um conjunto de técnicas que qualquer programador pode seguir. Ele busca encorajar projetos simples para pessoas minimamente sãs e normais que querem que seus códigos funcionem dentro do esperado. Não acho que é pedir muito, né?

Para que isso ocorra, precisamos seguir o passo-a-passo abaixo:

1. **Escreva um teste automático objetivo** antes de escrever o código. Ele irá falhar — *Nesse momento estamos na barra vermelha*.
2. **Escreva o código da forma mais preguiçosa possível** até o teste funcionar. Isso qualquer um pode fazer — *Nesse momento estamos na barra verde*.
3. **Remova a duplicação e melhore o código** no seu tempo. — *Assim atingimos a fase refatorar*.
4. **Repita o ciclo eternamente** até o fim dos seus dias.  
  
### Aprofundando no TDD

Deixando de lado as brincadeiras, trabalhar com TDD é dar pequenos passos para atingir os seus objetivos — segundo Kent Beck, o criador do TDD. Assim, buscamos criar uma série de testes simples que verificam se os pequenos passos foram dados.

Vamos pegar um exemplo bem simples: **ler um arquivo de texto e transformá-lo em lista separada por espaços**. Aplicando o TDD, nossos passos seriam:

1. Testar se consigo achar o arquivo.
2. Testar se consigo ler o arquivo.
3. Verificar se o texto está no formato esperado.
4. Verificar se consigo cortar o texto no local esperado (os espaços).
5. Verificar se a lista final possui os valores esperados.

Os testes são bem simples e objetivos, e o passo a passo seria implementar os testes um a um e fazê-los funcionar, da seguinte maneira:

1. Implementar o teste 1.
2. Criar o código mínimo para fazer o teste 1 passar. Nesse ponto, o código é o mínimo possível — pode retornar uma constante simples diretamente, se preciso. O que importa é ***o teste funcionar***.
3. Melhorar o código gradativamente, sem alterar o teste, ***até ter um resultado mínimo viável***.
4. Partir para implementar o teste 2.

Perceba que, a partir do momento que fazemos o teste funcionar, temos o caminho livre para refatorar e modificar o código, e a garantia de que o código vai funcionar é o teste. Também temos um passo a passo de como o código irá operar, podendo assim rastrear seu funcionamento.

Uma vez que implementamos o código, podemos implementar novos testes. Por exemplo: testar e verificar erros ou desvios no resultado. Bem, as possibilidades são infinitas.  

## Conhecendo o Pytest  

O [Pytest](https://docs.pytest.org/en/stable/) é uma estrutura de testes de software, ou seja, por meio de linha de comando o pytest encontra os testes, roda e mostra os resultados, além de permiter instalar plugins e instalar plugins de terceiros.  

### Tasks e os tipos de testes
A unidade do pytest é a ***task*** que é o aplicativo por linha de comando que executa um conjusto de tasks.  

Principais tipos de testes:
- ***Teste unitário:*** É o teste que verifica uma pequena parte do código, como uma função ou uma classe, de forma isolada do
resto do sistema.
- ***Teste de integração:*** É o teste que verifica uma parte maior do códigom nomalmente subsistema ou requisito do sistema. Ele é maior que um teste unitário e menor que um teste de sistema.
- **Teste de sistema (ponta a ponta):** É um teste que verifica todo o sistema em um abiente de teste, normalmente antes de liberar uma release ou projeto final. É o ambiente de teste mais próximo do usuário final.
- ***Teste funcional:*** é o teste que que verifica uma única funcionalidade de um sistema, como por exemplo adicionar, excluir ou atualizar um item.
- ***Teste subcutâneo:*** é o teste que não é executado na interface final do usuário, mas abaixo dela, como no caso de testar as API que alimentam a interface do usuário.  

O foco do pytest é realizar ***testes funcionais*** e ***testes subcutâneos***, embora possa realizar os demais testes.  

## Primeiros passos com pytest  

### O que fazer antes de começar?
O primeiro passo para usar o pyteste é criar um ambiente virtual, para isso basta executar o comando abaixo:  
```python
python -m venv venv
```  

Com isso será criado um abiente virtual isolado. Para iniciar basta usar: `venv\Scripts\activate` para iniciar o venv.  

Com o venv iniciado, basta instalar o pytest:
```python
pip install pytest
```  

Com isso podemos ir até a pasta onde se encontra o primeiro teste:
```
cd .\modulos\modulo_1\codigo\
```  

### Rodando o primeiro teste  
Para iniciar o primeiro teste basta rodar:  

```python
#pasta .\modulos\modulo_1\codigo\
py.test.exe .\teste_1.py
```
Perceba que esse teste irá funcionar pois `(1, 2, 3) == (1, 2, 3)` mas se alterarmos qualquer valor irá ocorrer um erro:  

```python
#pasta .\modulos\modulo_1\codigo\
py.test.exe .\teste_2.py
```
Você ainda consegue ver ainda mais detalhes ao usar -v:

```python
#pasta .\modulos\modulo_1\codigo\
py.test.exe -v .\teste_2.py
```