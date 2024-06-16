def add_user(username, password):
    with open('users.txt', 'a+') as file:
        if username in file:
            print("Username già esistente, riprovare con un altro username!")
            return False
        elif type(username) is str and type(password) is str:
            file.write(f"{username}:{password}\n")
            return True
        else: 
            print("C'è stato un errore")
            return False


def authenticate_user(username, password):
    with open('users.txt', 'r') as file:
        for line in file:
            stored_username, stored_password = line.strip().split(':')
            if stored_username == username and stored_password == password:
                return True
    return False
