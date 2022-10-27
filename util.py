

from random import randint
import socket


BUFFER_SIZE = 1024

def receiveBufferData(clientSocket):
    while True:
        data = clientSocket.recv(BUFFER_SIZE)
        if data:
            string = data.decode()
            print(f'string received by {clientSocket.getpeername()}: ', string)
            return string

def podeFalar(clientSocket):
    clientSocket.send('SPK'.encode('utf-8'))

def printMenu(clientSocket):
    i = None
    menu = "\n\n====================  TIRO E MOSCA  ====================\nSeja bem-vindo ao jogo de tira e mosca!\nEscolha uma opçao para prosseguir:\n[1] Jogo Individual\n[2] Dois Jogadores\n[3] Contra o computador\n[4] Regras\n[0] Sair\n"
    while i not in ['0','1','2','3','4']:
        
        if i == None:
            clientSocket.send((menu + '\nEscolha: ').encode('utf-8'))
        else:
            clientSocket.send(('\nEscolha uma opcao valida: ').encode('utf-8'))

        podeFalar(clientSocket)

        i = receiveBufferData(clientSocket)
        
    return i

def getClient(serverSocket: socket):
    serverSocket.listen()
    return serverSocket.accept()

def printRules(clientSocket):
    clientSocket.send(("\n====================  REGRAS  ====================\n\nO jogo é realizado em turnos, de forma que o usuário deve tentar adivinhar o número de três digitos do adversário. Para tal, sempre que for feito um palpite, este jogador receberá uma avaliação do palpite do tipo nTmM, onde T se refere à um tiro, M à uma mosca e n e m são números naturais que definem a quantidade de cada tiro ou mosca. Uma mosca significa que o jogador acertou um dígito e sua posição enquanto o tiro se refere a um dígito correto, mas na posição errada\n\nNo modo de jogador individual, o jogador tenta acertar um número aleatório definido no servidor.\n\nNo modo de dois jogadores, dois jogadores se enfrentam em turnos, um dando um palpite de cada vez, o primeiro que acertar o número do outro é o ganhador.\n\nPor fim, um modo contra o computador é também disponibilizado, de forma que o jogador joga contra um bot, assim como no modo de dois jogadores.").encode('utf-8'))

def checkGuess(guess, real):
    mosca = 0
    tiro = 0
    for i in range(3):
        for j in range(3):
            if guess[i] == real[j] and i==j:
                mosca = mosca + 1
            elif guess[i] == real[j]:
                tiro = tiro + 1
    return tiro, mosca

def createGuessingNumber():
    guessingNumber = ''
    for i in range(3):
        digit = ''
        while digit == '' or digit in guessingNumber:
            digit = str(randint(1,9))
        guessingNumber = guessingNumber + digit
    return guessingNumber

def verifyPattern(guess):
    if guess.isnumeric() and len(guess) == 3:
        if guess[0] != guess[1] and guess[0] != guess[2] and guess[1] != guess[2]:
            return True
    return False


def avaliation(tupleMoscaTiro):
    return f'{tupleMoscaTiro[0]}T{tupleMoscaTiro[1]}M'