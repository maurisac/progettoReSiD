import socket
import vlc
import threading
import os

SERVER_HOST = 'localhost'
SERVER_PORT = 9999
# SERVER_HOST = '192.168.128.237'
# SERVER_PORT = 12345

BUFFERSIZE = 1024

def play_stream():
    instance = vlc.Instance()
    player = instance.media_player_new()

    temp_file_path = '/tmp/stream.mp3'

    player.set_mrl(f'file://{temp_file_path}')
    player.play()

    while True:
        command = input("Comandi disponibili: play, pause, stop, forward, backward, quit\nTu: ").strip().lower()

        if command == 'play':
            player.play()
        elif command == 'pause':
            player.pause()
        elif command == 'stop':
            player.stop()
        elif command == 'forward':
            player.set_time(player.get_time() + 10000)  # Avanti di 10 secondi
        elif command == 'backward':
            player.set_time(player.get_time() - 10000)  # Indietro di 10 secondi
        elif command == 'quit':
            player.stop()
            break
        else:
            print("Comando non valido. Riprova.")

def receive_stream(sock):
    temp_file_path = '/tmp/stream.mp3'
    with open(temp_file_path, 'wb') as f:
        while True:
            data = sock.recv(BUFFERSIZE)
            if not data:
                break
            f.write(data)
    print("[INFO] Streaming terminato, file salvato in /tmp/stream.mp3")

def connection():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((SERVER_HOST, SERVER_PORT))

        while True:
            response = sock.recv(BUFFERSIZE).decode().strip()
            print(f"[SERVER] {response}")

            if "Verrai disconnesso." in response or "Arrivederci!" in response or "Connessione chiusa" in response:
                print("Disconnessione dal server.")
                break

            message = input("Tu: ")
            sock.sendall(message.encode())

            if 'Riproduco il file' in response:
                threading.Thread(target=play_stream).start()
                receive_stream(sock)

            if message.lower() == 'esci':
                break

connection()
