users = {
'valeska':{
    'name':'valeska',
    'password':'000'
    },
'maria':{
    'name':'mariazinha',
    'password':'111'
    }
}

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

