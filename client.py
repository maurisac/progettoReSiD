import socket
import subprocess
import threading

SERVER_HOST = 'localhost'
SERVER_PORT = 9999
BUFFERSIZE = 1024

def play_stream(file_path):
    subprocess.run(['vlc', file_path])

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
                break  # Dopo aver ricevuto lo stream, esci dal loop principale

            elif 'requiredInput' in response:
                    message = input("Tu: ")
                    sock.sendall(message.encode())
            else:
                print(f"[SERVER] {response}")


if __name__ == "__main__":
    connection()
