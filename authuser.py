def add_user(username, password):
    if not isinstance(username, str):
        return False

    with open('users.txt', 'a+') as file:
        file.seek(0)
        for line in file:
            parts = line.strip().split(':')
            if len(parts) != 2:
                continue
            stored_username, _ = parts
            if stored_username == username:
                return False
        file.write(f"{username}:{password}\n")
        return True


def authenticate_user(username, password):
    with open('users.txt', 'r') as file:
        for line in file:
            stored_username, stored_password = line.strip().split(':')
            if stored_username == username and stored_password == password:
                return True
    return False
