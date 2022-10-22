# -*- coding: utf-8 -*-
__author__ = "Filipe Ribeiro"

import socket, sys


HOST = '127.0.0.1'  # endereço IP
PORT = 20000        # Porta utilizada pelo servidor
BUFFER_SIZE = 1024  # tamanho do buffer para recepção dos dados

def enviarValorInicial(s):
    valor = input("Digite um valor para o oponente\n")
    while (len(str(valor)) != 3 or not str(valor).isdigit()):
            valor = input("Digite um valor para o oponente\n")
    s.send(valor.encode())
    while(True):
        esperandoValorJogador = s.recv(BUFFER_SIZE).decode('utf-8')
        if(esperandoValorJogador == "hora de jogar"):
            print(esperandoValorJogador)
            break
        else:
            print(esperandoValorJogador)
def main(argv): 
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))
            print("Servidor executando!")
            while(True):
                foiAceito = s.recv(BUFFER_SIZE).decode('utf-8')
                if(foiAceito == "Aceito"):
                    break
                else:
                    print("esperando jogador")
            while(True):
                enviarValorInicial(s)

                enviarPalpitesVerResultados(s)

            
    except Exception as error:
        print("Exceção - Programa será encerrado!")
        print(error)
        return

def enviarPalpitesVerResultados(s):
    qtdPalpites = 0
    while(True):
        texto = input("Digite um palpite: ")
        if(texto=="sair"):
            s.close()
            break
        while (len(str(texto)) != 3 or not str(texto).isdigit()):
            texto = input("Digite um palpite: ")
            if(texto=="sair"):
                s.close()
                break
        s.send(texto.encode()) #texto.encode - converte a string para bytes
        data = s.recv(BUFFER_SIZE)
        texto_string = data.decode('utf-8')
        if(texto_string == "esperando palpite do outro jogador"):
            print(texto_string)
            data = s.recv(BUFFER_SIZE)

        #texto_recebido = repr(data) #converte de bytes para um formato "printável"
        texto_string = data.decode('utf-8') #converte os bytes em string
        print(texto_string)
        data = s.recv(BUFFER_SIZE)
        qtdPalpites+=1
        if (data.decode('utf-8') == "Voce ganhou" or data.decode('utf-8') == "Voce perdeu"):
            print("{} com {} palpites".format(data.decode('utf-8'), qtdPalpites))
            data = s.recv(BUFFER_SIZE)
            print(data.decode('utf-8'))
            print('vai reiniciar o jogo')
            break

def jogoUmjogador(s):
    while(True):
        texto = input("Digite um palpite\n")
        while (len(str(texto)) != 3 or not str(texto).isdigit()):
            texto = input("Digite um palpite\n")
        print("enviado:"+ str(texto))
        s.send(texto.encode()) #texto.encode - converte a string para bytes
        data = s.recv(BUFFER_SIZE)
        texto_recebido = repr(data) #converte de bytes para um formato "printável"
        texto_string = data.decode('utf-8') #converte os bytes em string
        print(texto_recebido)
        if (texto == '000' or texto_string=='T3M0'):
            print('vai encerrar o socket cliente!')
            s.close()
            break

if __name__ == "__main__":   
    main(sys.argv[1:])