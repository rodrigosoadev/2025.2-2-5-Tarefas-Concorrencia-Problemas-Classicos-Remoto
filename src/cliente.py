import threading
import socket
import os
import time
import random
from dotenv import load_dotenv

class ClienteEstacionamento(threading.Thread):
    def __init__(self, id_cliente):
        threading.Thread.__init__(self)
        self.id_cliente = id_cliente

    def run(self):
        try:
            self.socket_cliente = criar_socket_cliente()
            
            # 1. Consulta
            vagas = self.consultar_vaga()
            print(f"[Cliente {self.id_cliente}] Vagas disponíveis: {vagas}")

            # 2. Tenta estacionar
            if self.pegar_vaga():
                print(f"[Cliente {self.id_cliente}] Estacionou com sucesso! ✅")
                self.passear()
                self.liberar_vaga()
                print(f"[Cliente {self.id_cliente}] Saiu e liberou a vaga. 👋")
            else:
                print(f"[Cliente {self.id_cliente}] Não encontrou vaga e foi embora. ❌")
            
            self.socket_cliente.close()
        except Exception as e:
            print(f"Erro no Cliente {self.id_cliente}: {e}")

    def consultar_vaga(self):
        self.socket_cliente.send("consultar_vaga".encode())
        return self.socket_cliente.recv(1024).decode()

    def pegar_vaga(self):
        self.socket_cliente.send("pegar_vaga".encode())
        return self.socket_cliente.recv(1024).decode() == "1"

    def liberar_vaga(self):
        self.socket_cliente.send("liberar_vaga".encode())
        return self.socket_cliente.recv(1024).decode() == "1"
    
    def passear(self):
        time.sleep(random.uniform(1, 3))

def criar_socket_cliente():
    load_dotenv()
    PORTA = int(os.getenv('PORT', 5000))
    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    cliente.connect(('localhost', PORTA))
    return cliente

def main():
    threads = []
    for i in range(50):
        c = ClienteEstacionamento(i)
        threads.append(c)
        c.start()
    
    for t in threads:
        t.join()

if __name__ == "__main__":
    main()