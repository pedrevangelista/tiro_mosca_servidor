import socket
import sys

HOST = "127.0.0.1"
PORT = 20000
BUFFER_SIZE = 1024

def main(argv):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))
            print("Servidor executando!")
            canSpeak = False
            while(True):       
                data = s.recv(BUFFER_SIZE)
                if data or canSpeak:
                    stringReceived = data.decode('utf-8')
                    print(stringReceived.replace('SPK', '').replace('CLS',''))
                    if "CLS" in stringReceived:
                        s.close()
                        break
                    elif "SPK" in stringReceived:
                        canSpeak = True
                    if canSpeak:
                        stringResponse = input()
                        s.send(stringResponse.encode('utf-8'))
                    canSpeak = False
                
                
    except Exception as error:
        print("Exceção - Programa será encerrado!")
        print(error)
        return


if __name__ == "__main__":   
    main(sys.argv[1:])