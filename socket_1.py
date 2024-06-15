import socket
import authuser

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
            message = client_socket.recv(1024).decode().strip()
            print(f"Messaggio ricevuto: {message}")

            if message.lower() == 'accedi':
                credential = []

                client_socket.sendall("Inserisci il tuo username: ".encode())
                username = client_socket.recv(1024).decode().strip()
                print(f"Username ricevuto: {username}")
                credential.append(username)

                client_socket.sendall("Inserisci la tua password: ".encode())
                password = client_socket.recv(1024).decode().strip()
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
                username = client_socket.recv(1024).decode().strip()
                print(f"Username ricevuto: {username}")
                credential.append(username)

                client_socket.sendall("Inserisci la tua password: ".encode())
                password = client_socket.recv(1024).decode().strip()
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


