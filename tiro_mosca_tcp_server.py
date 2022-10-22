# -*- coding: utf-8 -*-
__author__ = "Filipe Ribeiro"

import socket, sys, random
from threading import Thread
import time

HOST = '127.0.0.1'  # endereço IP
PORT = 20000        # Porta utilizada pelo servidor
BUFFER_SIZE = 1024  # tamanho do buffer para recepção dos dados

from threading import Thread
 
# custom thread
class ThreadWithReturnValue(Thread):
    
    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs={}, Verbose=None):
        Thread.__init__(self, group, target, name, args, kwargs)
        self._return = None

    def run(self):
        if self._target is not None:
            self._return = self._target(*self._args, **self._kwargs)
    def join(self, *args):
        Thread.join(self, *args)
        return self._return
    def verRetorno(self):
        return self._return

def verificarTirosMoscas(valorReal, valorDigitado):
    tiros = []
    moscas = []
    for i in range(0,3):
        if(valorDigitado[i]==valorReal[i]):
            moscas.append(valorReal[i])
    for i in range(0,3):
        for j in range(0,3):
            if(valorDigitado[i]==valorReal[j] and valorDigitado[i] not in moscas):
                tiros.append(valorReal[j])
    return (tiros,moscas)


def on_new_client(clientsocket,addr, client2):
    tiros = []
    moscas = []
    qtdPalpites = 0
    digito1 = random.randint(0,9)
    digito2 = random.randint(0,9)
    digito3 = random.randint(0,9)
    digitos = "{}{}{}".format(digito1, digito2, digito3)
    while True:
        try:

            data = clientsocket.recv(BUFFER_SIZE)
            if not data:
                break
            texto_recebido = data.decode('utf-8') # converte os bytes em string
            (tiros,moscas) = verificarTirosMoscas(str(digitos), str(texto_recebido))
            qtdPalpites+=1
            dados_acerto = 'T{}M{}'.format(len(tiros), len(moscas))
            print('{} - {}'.format(texto_recebido, dados_acerto))
            # envia o mesmo texto ao cliente 
            clientsocket.send(dados_acerto.encode())
            if(dados_acerto == "T0M3"):
                print("Acertou o numero com {} tentivas".format(qtdPalpites))
                clientsocket.close() 
                return 
               
                
        except Exception as error:
            print("Erro na conexão com o cliente!!")
            return

def jogoDoisClientes(client1, client2):
    qtdVitoriasJogador1 = 0
    qtdVitoriasJogador2 = 0
    while(True):
        palpites1=["   Você    |  Oponente "]
        palpites1.append("-----------|-----------")
        palpites2=["   Você    |  Oponente "]
        palpites2.append("___________|___________")
        caractereJoin = "\n"
        (valorClient1 ,valorClient2) =  obterValorInicialDosJogadores(client1, client2)
        print(valorClient1, valorClient2)
        client1.send("hora de jogar".encode())
        client2.send("hora de jogar".encode())
        while(True):
            (palpite1, palpite2) = obterValorPalpiteDosJogadores(client1, client2)
            (tiros1, moscas1) = verificarTirosMoscas(valorClient2, palpite1)
            (tiros2, moscas2) = verificarTirosMoscas(valorClient1, palpite2)
            dados_acerto1 = '{} - T{}M{}'.format(palpite1, len(tiros1), len(moscas1))
            dados_acerto2 = '{} - T{}M{}'.format(palpite2, len(tiros2), len(moscas2))
            palpites1.append("{} | {}".format(dados_acerto1, dados_acerto2))
            palpites2.append("{} | {}".format(dados_acerto2, dados_acerto1))
            client1.send(caractereJoin.join(palpites1).encode())
            client2.send(caractereJoin.join(palpites2).encode())
            if(dados_acerto1=="{} - T0M3".format(palpite1)):
                qtdVitoriasJogador1+=1
                print("jogador 1 ganhou")
                client1.send("Voce ganhou".encode())
                client2.send("Voce perdeu".encode())
                time.sleep(1)
                client2.send("Placar: Voce {} x {} Oponente".format(qtdVitoriasJogador2, qtdVitoriasJogador1).encode())
                client1.send("Placar: Voce {} x {} Oponente".format(qtdVitoriasJogador1, qtdVitoriasJogador2).encode())
                break
            elif(dados_acerto2=="{} - T0M3".format(palpite2)):
                qtdVitoriasJogador2+=1
                print("jogador 2 ganhou")
                client2.send("Voce ganhou".encode())
                client1.send("Voce perdeu".encode())
                time.sleep(1)
                client2.send("Placar: Voce {} x {} Oponente".format(qtdVitoriasJogador2, qtdVitoriasJogador1).encode())
                client1.send("Placar: Voce {} x {} Oponente".format(qtdVitoriasJogador1, qtdVitoriasJogador2).encode())
                break
            else:
                client1.send("continuar jogo".encode())
                client2.send("continuar jogo".encode())

def obterValorPalpiteDosJogadores(client1, client2):
    valorClient1 = 0
    valorClient2 = 0
    t1 = ThreadWithReturnValue(target=obterValorValido, args=(client1, valorClient1))
    t1.start()
    t2 = ThreadWithReturnValue(target=obterValorValido, args=(client2, valorClient2))
    t2.start()
    envioClient1 = False
    envioClient2 = False
    while(t1.is_alive() or t2.is_alive()):
        if(not t1.is_alive() and not envioClient1 and not envioClient2):
            client1.send("esperando palpite do outro jogador".encode())
            envioClient1 = True
        if(not t2.is_alive() and not envioClient2 and not envioClient1):
            client2.send("esperando palpite do outro jogador".encode())
            envioClient2 = True
    valorClient1 = t1.verRetorno()
    valorClient2 = t2.verRetorno()
    return (valorClient1, valorClient2)

def obterValorInicialDosJogadores(client1, client2):
    valorClient1 = 0
    valorClient2 = 0
    t1 = ThreadWithReturnValue(target=obterValorValido, args=(client1, valorClient1))
    t1.start()
    t2 = ThreadWithReturnValue(target=obterValorValido, args=(client2, valorClient2))
    t2.start()
    envioClient1 = False
    envioClient2 = False
    while(t1.is_alive() or t2.is_alive()):
        if(not t1.is_alive() and not envioClient1 and not envioClient2):
            client1.send("esperando jogador 2".encode())
            envioClient1 = True
        if(not t2.is_alive() and not envioClient2 and not envioClient1):
            client2.send("esperando jogador 1".encode())
            envioClient2 = True
    valorClient1 = t1.verRetorno()
    valorClient2 = t2.verRetorno()
    return (valorClient1, valorClient2)

def obterValorValido(client, valorClient):
    while((len(str(valorClient)) != 3 or not str(valorClient).isdigit())):
        valorClient = client.recv(BUFFER_SIZE)
        valorClient = valorClient.decode('utf-8')
    return valorClient
        
def main(argv):
    conexoes = 0
    clients = ['', '']
    addrs = ['', '']
    try:
        # AF_INET: indica o protocolo IPv4. SOCK_STREAM: tipo de socket para TCP,
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.bind((HOST, PORT))
           
            while(conexoes<2):
                server_socket.listen()
                clientsocket, addr = server_socket.accept()
                clients[conexoes] = clientsocket
                addrs[conexoes] = addr
                if(clientsocket):
                    conexoes+=1
                if(conexoes == 1):
                    clients[0].send("Esperando Jogador".encode())

            print('Conectado ao 1° cliente no endereço:', addrs[0])
            print('Conectado ao 2° cliente no endereço:', addrs[1])

            #t1 = Thread(target=on_new_client, args=(clients[0],addr[0],clients[1]))
            #t1.start()
            #t2 = Thread(target=on_new_client, args=(clients[1],addr[1],clients[0]))
            #t2.start()
            t1 = Thread(target=jogoDoisClientes, args=(clients[0],clients[1]))
            t1.start()
            clients[0].send("Aceito".encode())
            clients[1].send("Aceito".encode())
    except Exception as error:
        print("Erro na execução do servidor!!")
        print(error)        
        return             



if __name__ == "__main__":   
    main(sys.argv[1:])