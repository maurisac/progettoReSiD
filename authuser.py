def add_user(username, password):
    with open('users.txt', 'a') as file:
        file.write(f"{username}:{password}\n")

def authenticate_user(username, password):
    with open('users.txt', 'r') as file:
        for line in file:
            stored_username, stored_password = line.strip().split(':')
            if stored_username == username and stored_password == password:
                return True
    return False
