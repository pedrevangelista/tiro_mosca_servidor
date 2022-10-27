
from glob import glob
from http import client
import socket
from threading import Thread
import time
from individualGame import individualGame
from util import *


import re

HOST = "127.0.0.1"
PORT = 20000

AVAILABLE_PLAYERS = []
MATCHES_HAPPENING = []
#string received by <socket.socket fd=352, family=AddressFamily.AF_INET, type=SocketKind.SOCK_STREAM, proto=0, laddr=('127.0.0.1', 20000), raddr=('127.0.0.1', 51097)>


def playMultiplayerGame(playerOne, playerTwo):
    socket1 = playerOne[0]
    socket2 = playerTwo[0]
    username1 = playerOne[1]
    username2 = playerTwo[1]

    socket1.send(f'\nPartida encontrada com o jogador {username2}'.encode('utf-8'))
    socket2.send(f'\nPartida encontrada com o jogador {username1}'.encode('utf-8'))
    input()

def printMultiplayerHistory(clientSocket, username):
    print()

def isInMatch(user):
    for i in range(len(MATCHES_HAPPENING)):
        if user in MATCHES_HAPPENING[i]:
            return True
    return False

def multiplayerGameQueue(clientSocket, username):
    global AVAILABLE_PLAYERS
    global MATCHES_HAPPENING

    opponent = None
    if len(AVAILABLE_PLAYERS) >= 1:
        print(AVAILABLE_PLAYERS)
        opponent = AVAILABLE_PLAYERS.pop(0)
        MATCHES_HAPPENING.append((opponent, (clientSocket, username)))
        playMultiplayerGame(opponent, (clientSocket, username))
    else:
        AVAILABLE_PLAYERS.append((clientSocket, username))
        aux = True
        while (clientSocket, username) in AVAILABLE_PLAYERS:
            clientSocket.send('\nAguardando outro jogador...'.encode('utf-8'))
            time.sleep(2)
        while True:
            time.sleep(1)
            if not isInMatch((clientSocket, username)):
                break
    
    return

def multiplayerGame(clientSocket, username):
    option = None
    while True:
        clientSocket.send('\n\n====================  2 JOGADORES  ====================\nBem-vindo ao modo de jogo de dois jogadores!\n[1] Jogar\n[2] Histórico de partidas\n[0] Voltar ao menu principal'.encode('utf-8'))
        if option == None:
            clientSocket.send(('\nEscolha: ').encode('utf-8'))
        else:
            clientSocket.send(('\nEscolha uma opcao valida: ').encode('utf-8'))
        podeFalar(clientSocket)
        option = receiveBufferData(clientSocket)
        if option == '1':
            multiplayerGameQueue(clientSocket, username)
        elif option == '2':
            printMultiplayerHistory(clientSocket, username)
        elif option == '0':
            return

def on_new_client(clientSocket,clientAddr):
    username = None
    while True:
        clientSocket.send(('\nFavor inserir um nome de usuário com no mínimo três caracteres e máximo quinze, sem caracteres especiais.\nNome de usuário: SPK').encode('utf-8'))
        username = receiveBufferData(clientSocket)
        if username.isalnum():
            break
    while True:
        try:
            gameType = printMenu(clientSocket)
            if gameType == '0':
                clientSocket.send(('\nConexão encerrada com o servidorCLS').encode('utf-8'))
                print(f'connection closed with {clientSocket.getpeername()}')
                clientSocket.close()
                return
            elif gameType == '1':
                individualGame(clientSocket, username)
            elif gameType == '2':
                multiplayerGame(clientSocket, username)
            elif gameType == '3':
                print()
            elif gameType == '4':
                printRules(clientSocket)
                

        except Exception as error:
            print("Erro na conexão com o cliente!!")
            return

# Main method to create the TCP connection and associate the respective Thread to a new connection client-server.
def main():
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as serverSocket:
            serverSocket.bind((HOST, PORT))
            while True:
                clientSocket, clientAddr = getClient(serverSocket=serverSocket)
                t = Thread(target=on_new_client, args=(clientSocket, clientAddr))
                t.start()
    except Exception as error:
        print(f'Server inicialization error: {error}')


if __name__ == "__main__":
    main()