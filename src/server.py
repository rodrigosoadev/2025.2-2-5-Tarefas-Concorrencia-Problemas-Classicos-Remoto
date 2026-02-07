#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import socket
import os
import threading
from dotenv import load_dotenv

# Configurações Globais
VAGAS_TOTAIS = 10
vagas_disponiveis = VAGAS_TOTAIS
vagas_lock = threading.Lock() # Lock para evitar condição de corrida

def escutar_cliente(nova_conexao, endereco):
    global vagas_disponiveis
    print(f'Cliente conectado de {endereco}')
    
    try:
        while True:
            mensagem = nova_conexao.recv(1024)
            if not mensagem:
                break            
            comando = mensagem.decode("utf-8").strip()
            
            resposta = "-1" # Padrão para erro

            # Seção Crítica protegida por Lock
            with vagas_lock:
                if comando == 'consultar_vaga':
                    resposta = str(vagas_disponiveis)
                
                elif comando == 'pegar_vaga':
                    if vagas_disponiveis > 0:
                        vagas_disponiveis -= 1
                        resposta = "1" # Sucesso
                    else:
                        resposta = "0" # Lotado
                
                elif comando == 'liberar_vaga':
                    if vagas_disponiveis < VAGAS_TOTAIS:
                        vagas_disponiveis += 1
                        resposta = "1" # Sucesso
                    else:
                        resposta = "0" # Erro: Estacionamento já vazio

            nova_conexao.send(resposta.encode('utf-8'))
            
            # Se liberou a vaga, encerramos essa conexão conforme o protocolo
            if comando == 'liberar_vaga' and resposta == "1":
                break
                
    finally:
        nova_conexao.close()
        print(f'Cliente {endereco} desconectado')

def iniciar_servidor():
    load_dotenv()
    PORTA = int(os.getenv('PORT', 5000))
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    servidor.bind(('localhost', PORTA))
    servidor.listen(50) # Aumentado para suportar a fila de 50 clientes
    print(f'Servidor escutando na porta {PORTA}')
    return servidor

def main():
    servidor = iniciar_servidor()
    try:
        while True:
            nova_conexao, endereco = servidor.accept()
            thread = threading.Thread(target=escutar_cliente, args=(nova_conexao, endereco))
            thread.daemon = True
            thread.start()
    finally:
        servidor.close()

if __name__ == '__main__':
    main()