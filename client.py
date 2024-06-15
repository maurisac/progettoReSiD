import socket

SERVER_HOST = 'localhost'
SERVER_PORT = 9999

def connection():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((SERVER_HOST, SERVER_PORT))
        
        while True:
            response = sock.recv(1024).decode().strip()
            print(f"Server: {response}")
            
            message = input("Tu: ")
            sock.sendall(message.encode())
            
            if message.lower() == 'esci':
                break
            
            if message.lower() == 'accedi':
                response = sock.recv(1024).decode().strip()
                print(f"Server: {response}")

                username = input()
                sock.sendall(username.encode())
                
                response = sock.recv(1024).decode().strip()
                print(f"Server: {response}")
                
                password = input()
                sock.sendall(password.encode())
                
                response = sock.recv(1024).decode().strip()
                print(f"Server: {response}")

            if message == 'Autenticato!':
                break

connection()


