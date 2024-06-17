import socket
import vlc
import threading

SERVER_HOST = 'localhost'
SERVER_PORT = 9999

BUFFERSIZE = 1024

def play_stream():
    instance = vlc.Instance()
    player = instance.media_player_new()

    # Configura il player per ricevere dati da un buffer o flusso in tempo reale
    player.set_mrl('file:///tmp/stream.mp3')  # Puoi usare un file temporaneo come buffer

    player.play()
    
    # Continua a riprodurre fino a quando c'è uno stream disponibile
    while player.is_playing():
        continue

def receive_stream(sock):
    with open('/tmp/stream.mp3', 'wb') as f:  # Salva i dati in un file temporaneo
        while True:
            data = sock.recv(BUFFERSIZE)
            if not data:
                break
            f.write(data)

def connection():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((SERVER_HOST, SERVER_PORT))

        while True:
            response = sock.recv(BUFFERSIZE).decode().strip()
            print(f"Server: {response}")

            if "Verrai disconnesso." in response or "Arrivederci!" in response or "Connessione chiusa" in response:
                print("Disconnessione dal server.")
                break

            if "menu" in response or "successo" in response:
                continue

            message = input("Tu: ")
            sock.sendall(message.encode())

            if message == '1':  # Se il client sceglie di avviare lo streaming
                threading.Thread(target=play_stream).start()
                receive_stream(sock)  # Inizia a ricevere lo stream

            if message.lower() == 'esci':
                break

connection()
