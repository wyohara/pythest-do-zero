#!/usr/bin/env python3

import pytest
import socket
import threading
import time
from typing import List, Optional

# =======================================================================
#           Classes para simular um servidor TCP simples
# =======================================================================

class TCPServer:
    """
    Servidor TCP que gerencia a si mesmo - simplificado
    """
    
    def __init__(self, port: int = 8888):
        self.porta = port
        self.socket = None
        self.thread = None
        self.running = False
        self.mensagens: List[str] = []
    
    def start(self):
        """Inicia o servidor em uma thread separada."""
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.socket.bind(('localhost', self.porta))
            self.socket.listen(1)
            self.running = True
            
            self.thread = threading.Thread(target=self._aceitar_conexoes)
            self.thread.daemon = True
            self.thread.start()
            time.sleep(0.1)
        except Exception as e:
            print(f"Erro ao iniciar servidor na porta {self.porta}: {e}")
            self.running = False
    
    def _aceitar_conexoes(self):
        """Aceita conexões e recebe mensagens."""
        while self.running:
            try:
                self.socket.settimeout(1.0)
                client_socket, address = self.socket.accept()
                data = client_socket.recv(1024)
                if data:
                    self.mensagens.append(data.decode('utf-8'))
                client_socket.close()
            except socket.timeout:
                continue
            except Exception as e:
                if self.running:
                    print(f"Erro na conexão: {e}")
                break
    
    def enviar_mensagem(self, message: str, target: 'TCPServer'):
        """Envia uma mensagem para outro servidor."""
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.connect(('localhost', target.porta))
                sock.send(message.encode('utf-8'))
                return True
        except Exception as e:
            print(f"Erro ao enviar mensagem para porta {target.porta}: {e}")
            return False
    
    def verifica_mensagens(self, message: str) -> bool:
        """Verifica se uma mensagem foi recebida."""
        return message in self.mensagens
    
    def limpar_mensagens(self):
        """Limpa as mensagens recebidas."""
        self.mensagens.clear()
    
    def stop(self):
        """Para o servidor e libera recursos."""
        self.running = False
        if self.socket:
            self.socket.close()
        if self.thread:
            self.thread.join(timeout=1)

# =============================================
#   fixture VERSÃO PROBLEMÁTICA - monolítica
# =============================================

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
    
    # Teardown - PODE NÃO EXECUTAR se houver erro nas mensagens
    servidor_2.limpar_mensagens()
    servidor_1.stop()
    servidor_2.stop()


def test_mensagem_problematica(setup_problematico):
    server2, message = setup_problematico
    assert message in server2.mensagens
    print(f"[TESTE] Mensagem recebida: {server2.mensagens}")


# =============================================
#  VERSÃO CORRETA (Fixtures atomicas)
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