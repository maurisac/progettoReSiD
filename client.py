import socket
import subprocess
import threading
import time

SERVER_HOST = 'localhost'
SERVER_PORT = 9999
BUFFERSIZE = 4096

def play_stream(sock):
    process = subprocess.Popen(
        ['vlc', '--file-caching=3000', '-'], # Buffering might be needed
        stdin=subprocess.PIPE,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

    try:
        while True:
            data = sock.recv(BUFFERSIZE)
            if not data:
                break
            process.stdin.write(data)
    except Exception as e:
        print(f"[ERROR] Errore durante lo streaming: {e}")
    finally:
        process.stdin.close()
        process.wait()

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
                play_stream(sock)
                break

            elif 'requiredInput' in response:
                message = input("Tu: ")
                sock.sendall(message.encode())
            else:
                print(f"[SERVER] {response}")

if __name__ == "__main__":
    connection()
