import socket
import subprocess
import threading
import psutil
import time

SERVER_HOST = '192.168.1.72'
SERVER_PORT = 12345
BUFFERSIZE = 1024

def play_stream(file_path):
    process = subprocess.Popen(['vlc', file_path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    # Monitoraggio del processo VLC
    while True:
        if process.poll() is not None:
            # Il processo VLC è terminato, esci dal loop
            break
        time.sleep(1)

def receive_stream(sock):
    temp_file_path = '/tmp/stream.mp3'
    with open(temp_file_path, 'wb') as f:
        while True:
            data = sock.recv(BUFFERSIZE)
            if not data:
                break
            f.write(data)
    threading.Thread(target=play_stream, args=(temp_file_path,)).start()

def connection():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((SERVER_HOST, SERVER_PORT))

        while True:
            response = sock.recv(BUFFERSIZE).decode(errors='ignore').strip()

            if "Verrai disconnesso." in response or "Arrivederci!" in response or "Connessione chiusa" in response:
                print(f"[SERVER] {response}")
                print("Disconnessione dal server.")
                break

            elif 'Riproduco il file' in response:
                print(f"[SERVER] {response}")
                receive_stream(sock)
                break

            elif 'requiredInput' in response:
                    message = input("Tu: ")
                    sock.sendall(message.encode())
            else:
                print(f"[SERVER] {response}")


if __name__ == "__main__":
    connection()
