import socket
import vlc

def start_client():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(("localhost", 9999))  # Sostituisci con l'indirizzo del server

    while True:
        response = client.recv(4096).decode()
        if "Username" in response:
            username = input(response)
            client.send(username.encode())
        elif "Password" in response:
            password = input(response)
            client.send(password.encode())
        elif "Autenticazione riuscita" in response:
            print(response)
            break
        else:
            print(response)

    # Codice per ricevere lo stream audio e riprodurlo con VLC
    # ...

if __name__ == "__main__":
    start_client()
