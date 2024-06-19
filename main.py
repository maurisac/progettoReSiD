import socket
from threading import Thread, Lock
import time
import authuser
import fileHandler
import os

BUFFERSIZE = 1024
MUTEX = Lock()

SERVER_HOST = '0.0.0.0'
SERVER_PORT = 9999

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((SERVER_HOST, SERVER_PORT))
server.listen(5)
print(f"Server in ascolto all'indirizzo: {SERVER_HOST}:{SERVER_PORT}")

def send_message(sock, message):
    sock.sendall(message.encode())

def handleClient(clientSock, clientAddr):
    print(f"[INFO] Connessione accettata da: {clientAddr}")
    try:
        send_message(clientSock, "Inserire modalità:\nRegistrazione\nAccedi\nEsci")
        time.sleep(0.1)
        send_message(clientSock, "requiredInput")
        mode = clientSock.recv(BUFFERSIZE).strip().decode('utf-8')

        if mode.lower() not in ['registrazione', 'accedi', 'esci']:
            send_message(clientSock, "Operazione non valida. Verrai disconnesso.")
            clientSock.close()
            return

        if mode.lower() == 'esci':
            send_message(clientSock, "Arrivederci!")
            clientSock.close()
            return
        if mode:
            send_message(clientSock, "Username:")
            time.sleep(0.1)
            send_message(clientSock, "requiredInput")
            username = clientSock.recv(BUFFERSIZE).strip().decode('utf-8')

            send_message(clientSock, "Password:")
            time.sleep(0.1)
            send_message(clientSock, "requiredInput")
            password = clientSock.recv(BUFFERSIZE).strip().decode('utf-8')

        with MUTEX:
            if mode.lower() == 'registrazione':
                if not authuser.add_user(username, password):
                    send_message(clientSock, "Errore: registrazione fallita, Verrai disconnesso.")
                    clientSock.close()
                    return
                send_message(clientSock, "Registrazione effettuata con successo!")
            elif mode.lower() == 'accedi':
                if not authuser.authenticate_user(username, password):
                    send_message(clientSock, "Errore: autenticazione fallita, Verrai disconnesso.")
                    clientSock.close()
                    return
                send_message(clientSock, "Accesso effettuato con successo!")

        menu(username, clientSock, clientAddr)

    except Exception as e:
        print(f"[ERROR] Errore durante la gestione del client {clientAddr}: {e}")
    finally:
        print(f"[INFO] Connessione chiusa con: {clientAddr}")

def menu(username, clientSock, clientAddr):
    send_message(clientSock, f"Benvenuto {username}, inserisci l'operazione che vuoi effettuare:\n1: Streaming audio\n2: Esci")
    time.sleep(0.1)
    send_message(clientSock, "requiredInput")
    while True:
        try:
            mode = clientSock.recv(BUFFERSIZE).strip().decode('utf-8')

            if mode == '1':
                streaming(username, clientSock, clientAddr)
            elif mode == '2':
                send_message(clientSock, "Connessione chiusa.")
                break
            else:
                send_message(clientSock, "Operazione non valida. Riprova.")
        except Exception as e:
            print(f"[ERROR] Errore durante il menu per il client {clientAddr}: {e}")
            break
    clientSock.close()

def streaming(username, clientSock, clientAddr):
    files = fileHandler.listFiles('./files')
    files_list_str = '\n'.join(f"ID: {i} \tAudio: {file_name}" for i, file_name in enumerate(files))
    send_message(clientSock, f"Scegli l'ID dell'audio da riprodurre\n{files_list_str}")
    time.sleep(0.1)
    send_message(clientSock, "requiredInput")
    chosenAudioId = clientSock.recv(BUFFERSIZE).strip().decode('utf-8')
    send_message(clientSock, f"Riproduco il file {chosenAudioId}")

    try:
        chosen_audio_id = int(chosenAudioId)
        if 0 <= chosen_audio_id < len(files):
            chosen_audio = files[chosen_audio_id]
            file_path = os.path.abspath(f'./files/{chosen_audio}')

            print(f"[INFO] L'utente {username} ha scelto di riprodurre: {chosen_audio}")

            with open(file_path, 'rb') as f:
                while True:
                    data = f.read(BUFFERSIZE)
                    if not data:
                        break
                    clientSock.sendall(data)

            send_message(clientSock, "Streaming terminato.")
        else:
            send_message(clientSock, "ID non valido. Connessione chiusa.")
    except ValueError:
        send_message(clientSock, "Input non valido. Connessione chiusa.")
    except Exception as e:
        print(f"[ERROR] Errore durante lo streaming per il client {clientAddr}: {e}")
        send_message(clientSock, "Errore durante lo streaming. Connessione chiusa.")

    clientSock.close()

while True:
    client_socket, client_address = server.accept()
    client_thread = Thread(target=handleClient, args=(client_socket, client_address))
    client_thread.start()
