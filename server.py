import socket
import threading
import vlc
import pam

def handle_client(client_socket, address):
    print(f"Connessione accettata da {address}")

    # Autenticazione PAM
    p = pam.pam()
    client_socket.send(b"Username: ")
    username = client_socket.recv(1024).decode().strip()
    client_socket.send(b"Password: ")
    password = client_socket.recv(1024).decode().strip()

    if not p.authenticate(username, password):
        client_socket.send(b"Autenticazione fallita\n")
        client_socket.close()
        return

    client_socket.send(b"Autenticazione riuscita\n")

    # Inizia lo streaming audio
    media = vlc.MediaPlayer("test.mp3")  # Sostituisci con il file audio desiderato
    media.play()

    while True:
        # Codice per inviare lo stream audio ai client
        # ...

        if not media.is_playing():
            break

    media.stop()
    client_socket.close()

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("0.0.0.0", 9999))
    server.listen(5)
    print("Server in ascolto su porta 9999")

    while True:
        client_socket, addr = server.accept()
        client_handler = threading.Thread(target=handle_client, args=(client_socket, addr))
        client_handler.start()

if __name__ == "__main__":
    start_server()
