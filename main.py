#codice principale del server



#per prima cosa c'è la connessione col client

#autenticazione (con thread apposito che gestisce il file degli utenti con mutex) e poi menù di scelta per scegliere il video da riprodurre. Scelto il video, si avvia lo streaming

import authuser
import socket

from threading import Thread, Lock

BUFFERSIZE = 1024
MUTEX = Lock()

def handleClient(clientSock, clientAddr):
    global MUTEX
    print(f"[INFO] Connessione accettata da: {clientAddr}")
    # Autenticazione semplice
    try:
        clientSock.send(b"Inserire modalita registrazione/accesso: ")
        mode = clientSock.recv(BUFFERSIZE).strip().decode('utf-8')

        clientSock.send(b"Username: ")
        username_from_client = clientSock.recv(BUFFERSIZE).strip().decode('utf-8')
        
        clientSock.send(b"Password: ")
        password_from_client = clientSock.recv(BUFFERSIZE).strip().decode('utf-8')

    
        with MUTEX:
            if mode.lower() == 'registrazione':
                if not authuser.add_user(username_from_client, password_from_client):
                    clientSock.send(b"Errore")
                    return -1
                clientSock.send(b"Registrazione effettuata con successo!")
                menu(username_from_client, clientSock, clientAddr)

            elif mode.lower() == 'accesso':
                if not authuser.authenticate_user(username_from_client, password_from_client):
                    clientSock.send(b"Errore")
                    return -1
                clientSock.send(b"Accesso eseguito correttamente")
                menu(username_from_client, clientSock, clientAddr)

            else:
                print("Le operazioni disponibili sono registrazione/accesso")
                clientSock.close()


    except Exception as e:
        print(f"[ERROR] Errore durante la gestione del client {clientAddr}: {e}")
    
    finally:
        clientSock.close()
        print(f"[INFO] Connessione chiusa con: {clientAddr}")


def menu(username, clientSock, clientAddr):
    clientSock.sendall(f"Benvenuto {username}, inserisci l'operazione che vuoi effettuare:\n1: Streaming audio\n2:Esci".encode())
    mode = clientSock.recv(BUFFERSIZE).strip().decode('utf-8')
    
    if mode.lower() == '1' or mode.lower().startswith('streaming'):
        pass #streaming()
    elif mode.lower() == '2' or mode.lower().startswith('esci'):
        clientSock.close()


def streaming(username, clientSock, clientAddr):
    clientSock.sendall(f"Scegli l'ID dell'audio da riprodurre: ".encode())
    with open("audios.txt", "r") as file:
        audios = []
        for _ in file.read():
            i = 0
            clientSock.sendall(f"ID: {i}, audio '{_}'".encode())
            audios.append(_)
            i = i + 1
        chosenAudio = clientSock.recv(BUFFERSIZE).strip().decode('utf-8')
        
        #logica di streaming (apertura finestra vlc-->streaming-->chiusura)
        



SERVER_HOST = '0.0.0.0'
SERVER_PORT = 9999

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((SERVER_HOST, SERVER_PORT))
server.listen(5)
print(f"Server in ascolto all'indirizzo: {SERVER_HOST}:{SERVER_PORT}")

while True:
    client_socket, client_address = server.accept()
    print(f"Connessione accettata da: {client_address}")
    try:
        while True:
            client_socket.sendall("Benvenuto! Se hai già un profilo inserisci 'accedi', in caso contrario inserisci 'registrati'. Se desideri uscire inserisci 'esci'.".encode())
            message = client_socket.recv(BUFFERSIZE).decode().strip()
            print(f"Messaggio ricevuto: {message}")

            if message.lower() == 'accedi':
                credential = []

                client_socket.sendall("Inserisci il tuo username: ".encode())
                username = client_socket.recv(BUFFERSIZE).decode().strip()
                print(f"Username ricevuto: {username}")
                credential.append(username)

                client_socket.sendall("Inserisci la tua password: ".encode())
                password = client_socket.recv(BUFFERSIZE).decode().strip()
                print(f"Password ricevuta: {password}")
                credential.append(password)

                print(f"Credenziali ricevute: {credential}")
                client_socket.sendall("Credenziali ricevute".encode())

                if authuser.authenticate_user(credential[0],credential[1]) == True:
                    client_socket.sendall('Autenticato!'.encode())
                else:
                    client_socket.sendall('Nope!'.encode())

                break
                

            elif message.lower() == 'registrati':
                credential = []

                client_socket.sendall("Inserisci il tuo username: ".encode())
                username = client_socket.recv(BUFFERSIZE).decode().strip()
                print(f"Username ricevuto: {username}")
                credential.append(username)

                client_socket.sendall("Inserisci la tua password: ".encode())
                password = client_socket.recv(BUFFERSIZE).decode().strip()
                print(f"Password ricevuta: {password}")
                credential.append(password)

                print(f"Credenziali ricevute: {credential}")
                client_socket.sendall("Credenziali ricevute".encode())

                authuser.add_user(credential[0],credential[1])
                client_socket.sendall("aggiunto!".encode())

                break
                
            elif message.lower() == 'esci' or not message:
                client_socket.sendall("Connessione chiusa.".encode())
                break


    except Exception as e:
        print(f"Errore: {e}")
    finally:
        client_socket.close()
        print(f"Connessione chiusa da: {client_address}")




