from util import *
from datetime import datetime
from msilib.schema import Error


def playIndividualGame(clientSocket, userName):
    guessingNumber = createGuessingNumber()
    print(f'{clientSocket.getpeername()} - guessingNumber - {guessingNumber}')
    clientSocket.send('\nO número foi gerado!'.encode('utf-8'))
    guessingList = '\nLista de Palpites:'
    roundsCounter = 1
    gameCounter = 1
    guess = ''
    while True:
        aux = True
        if roundsCounter == 1:
            clientSocket.send(f'\n\n============ JOGO {gameCounter} ============'.encode('utf-8'))
            clientSocket.send(f'\nDigite \'proximo\' durante a partida para pular para próximo número ou \'sair\' para voltar ao menu. '.encode('utf-8'))
        while not verifyPattern(guess):
            clientSocket.send(f'\nPalpite {roundsCounter}: SPK'.encode('utf-8'))
            guess = receiveBufferData(clientSocket)
            if guess == 'sair':
                    return
            elif guess == 'proximo':
                guess = ''
                gameCounter = gameCounter + 1
                roundsCounter = 1
                guessingNumber = createGuessingNumber()
                print(f'{clientSocket.getpeername()} - guessingNumber - {guessingNumber}')
                clientSocket.send('\nO número foi gerado!'.encode('utf-8'))
                guessingList = '\nLista de Palpites:'
                aux = False
                break
        if guess == guessingNumber:
            option = ''
            while option != 'sair' and option != 'proximo':
                clientSocket.send(f'\nParabéns, você acertou o número! O número era {guessingNumber}. Digite \'proximo\' para continuar ou \'sair\' para voltar ao menu.\nSPK'.encode('utf-8'))
                with open(f'user_data\individual_game\{userName}.txt', 'a') as userData:
                    userData.write(f'{datetime.now().strftime("%d/%m/%Y %H:%M:%S")}   |   {guessingNumber}    |    {roundsCounter}\n')
                    userData.close()
                option = receiveBufferData(clientSocket)
                if option == 'sair':
                    return
                elif option == 'proximo':
                    guess = ''
                    gameCounter = gameCounter + 1
                    roundsCounter = 1
                    guessingNumber = createGuessingNumber()
                    print(f'{clientSocket.getpeername()} - guessingNumber - {guessingNumber}')
                    clientSocket.send('\nO número foi gerado!'.encode('utf-8'))
                    guessingList = '\nLista de Palpites:'
        elif aux:
            roundsCounter = roundsCounter + 1
            guessAvaliation = avaliation(checkGuess(guess, guessingNumber))
            guessingList = guessingList + f'\n{guess} - {guessAvaliation}'
            clientSocket.send(('\n' + guessingList).encode('utf-8'))
            guess = ''

def printGameHistory(clientSocket, userName):
    clientSocket.send('\n\n================  HISTÓRICO DO JOGADOR  ================'.encode('utf-8'))
    clientSocket.send('\n====   Horário   ======  Número  ====  Palpites  ==='.encode('utf-8'))
    try:
        with open(f'user_data\individual_game\{userName}.txt') as file:
            for line in file:
                clientSocket.send(line.encode('utf-8'))
            file.close()
    except Error as error:
        print(error)


def individualGame(clientSocket, username):
    option = None
    while True:
        clientSocket.send('\n\n====================  JOGO INDIVIDUAL  ====================\nBem-vindo ao modo de jogo individual!\n[1] Jogar\n[2] Histórico de partidas\n[0] Voltar ao menu principal'.encode('utf-8'))
        if option == None:
            clientSocket.send(('\nEscolha: ').encode('utf-8'))
        else:
            clientSocket.send(('\nEscolha uma opcao valida: ').encode('utf-8'))
        podeFalar(clientSocket)
        option = receiveBufferData(clientSocket)
        if option == '1':
            playIndividualGame(clientSocket, username)
        elif option == '2':
            printGameHistory(clientSocket, username)
        elif option == '0':
            return