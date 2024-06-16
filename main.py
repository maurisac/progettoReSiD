#codice principale del server
#per prima cosa c'è la connessione col client

#autenticazione (con thread apposito che gestisce il file degli utenti con mutex) e poi menù di scelta per scegliere il video da riprodurre. Scelto il video, si avvia lo streaming

import socket
from threading import Thread, Lock
import authuser
import fileHandler

BUFFERSIZE = 1024
MUTEX = Lock()

SERVER_HOST = '0.0.0.0'
SERVER_PORT = 9999

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((SERVER_HOST, SERVER_PORT))
server.listen(5)
print(f"Server in ascolto all'indirizzo: {SERVER_HOST}:{SERVER_PORT}")

def handleClient(clientSock, clientAddr):
    global MUTEX
    print(f"[INFO] Connessione accettata da: {clientAddr}")
    try:
        clientSock.send(b"Inserire modalita: 'registrazione' o 'accedi': ")
        mode = clientSock.recv(BUFFERSIZE).strip().decode('utf-8')

        if mode.lower() not in ['registrazione', 'accedi']:
            clientSock.send(b"Operazione non valida. Verrai disconnesso.")
            clientSock.close()
            return
        elif mode.lower() == 'esci':
            clientSock.send(b"Arrivederci!.")
            clientSock.close()
            return
        

        clientSock.send(b"Username: ")
        username = clientSock.recv(BUFFERSIZE).strip().decode('utf-8')
        
        clientSock.send(b"Password: ")
        password = clientSock.recv(BUFFERSIZE).strip().decode('utf-8')


        with MUTEX:
            if mode.lower() == 'registrazione':
                if authuser.add_user(username, password) == False:
                    clientSock.send(b"Errore: registrazione fallita, Verrai disconnesso.")
                    MUTEX.release()
                    return
                clientSock.send(b"Registrazione effettuata con successo!")
                MUTEX.release()
                menu(username, clientSock, clientAddr)
            elif mode.lower() == 'accedi':
                if not authuser.authenticate_user(username, password):
                    clientSock.send(b"Errore: autenticazione fallita, Verrai disconnesso.")
                    MUTEX.release()
                    return
                clientSock.send(b"Accesso effettuato con successo!")
                MUTEX.release()
                menu(username, clientSock, clientAddr)
            else:
                clientSock.send(b"Operazione non valida. Disconnessione.")
                MUTEX.release()
                return
            
    except Exception as e:
        print(f"[ERROR] Errore durante la gestione del client {clientAddr}: {e}")


    finally:
        clientSock.close()
        print(f"[INFO] Connessione chiusa con: {clientAddr}")




def menu(username, clientSock, clientAddr):
    clientSock.sendall(f"\nBenvenuto {username}, inserisci l'operazione che vuoi effettuare:\n1: Streaming audio\n2: Esci\n".encode())
    while True:
        mode = clientSock.recv(BUFFERSIZE).strip().decode('utf-8')
        if mode == '1':
            streaming(username, clientSock, clientAddr)
        elif mode == '2':
            clientSock.sendall(b"Connessione chiusa.")
            break
        else:
            clientSock.sendall(b"Operazione non valida. Riprova.")




def streaming(username, clientSock, clientAddr):
    clientSock.sendall(b"Scegli l'ID dell'audio da riprodurre: ")
    # clientSock.sendall(f"{}".encode())
    fileHandler.listFiles('./files')
    chosenAudio = clientSock.recv(BUFFERSIZE).strip().decode('utf-8')
    # Logica di streaming (es. apertura finestra VLC, streaming, chiusura)
    # clientSock.sendall(f"Audio scelto: {audios[int(chosenAudio)].strip()}".encode())




while True:
    client_socket, client_address = server.accept()
    client_thread = Thread(target=handleClient, args=(client_socket, client_address))
    client_thread.start()




