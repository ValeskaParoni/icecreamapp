from werkzeug.security import generate_password_hash, check_password_hash

class User:
    def __init__(self, username, password, name):
        self.username = username
        self.set_password(password)
        self.name = name

    def set_password(self, password):
        self.pw_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.pw_hash, password)


errors = {
'username':False,
'password':False
}

def clear_error():
    errors['username'] = False
    errors['password'] = False

def new_user(username, password, name):
    clear_error()
    new_user = {}
    if username in users:
        errors['username'] = True
        return False
    users[username] = {}
    users[username]['password'] = password
    users[username]['name'] = name
    return True


def check_user(username, password):
    clear_error()
    if username in users:
        if users[username]['password'] == password:
            return True
        else:
            errors['password'] = True
            return False
    else:
       errors['username'] = True
       return False

def get_name(username):
    clear_error()
    if username in users:
        return users[username]['name']
    else:
        errors['username'] = True
        return 'Undefined'

