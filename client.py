import socket

SERVER_HOST = 'localhost'
SERVER_PORT = 9999

def connection():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((SERVER_HOST, SERVER_PORT))

        while True:

            response = sock.recv(1024).decode().strip()
            print(f"Server: {response}")

            if "Verrai disconnesso." in response or "Arrivederci!" in response or "Connessione chiusa" in response:
                print("Disconnessione dal server.")
                break

            if "menu." not in response or "successo!" not in response:
                message = input("Tu: ")
                sock.sendall(message.encode())
            
            if message.lower() == 'esci':
                break

connection()


