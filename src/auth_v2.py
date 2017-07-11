from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from routes import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True)
    name = db.Column(db.String(100), unique=False)
    pw_hash = db.Column(db.String(300), unique=False)

    def __init__(self, username, password_hash, name):
        self.username = username
        self.pw_hash = password_hash
        self.name = name

    def _check_password(self, password):
        return check_password_hash(self.pw_hash, password)

    def _get_name(self):
        return self.name

'''


def create_user(username, password, name):
    if not _get_user_by_username(username):
        password_hash = generate_password_hash(password)
        cursor.execute("insert into user(username, password_hash, name) values(?, ?, ?)", (username, password_hash, name))
        db_connection.close()
        return User(username, password_hash, name)
    return None

def _get_user_by_username(username):
    db_connection = sqlite3.connect('../user.db')
    cursor = db_connection.cursor()
    cursor.execute("select * from user where username=?", [username])

    if cursor.fetchall():
        user_data = cursor.fetchall()[0]
        name = user_data[1]
        password_hash = user_data[2]
        return User(username, password_hash, name)

    return None

def get_user_by_username(username):
    user = _get_user_by_usarname(username)
    db_connection.close()
    return user


print ("1: criar usuario")
print (create_user('uservaleska', 'senha', 'nomevaleska'))
print ("2: criar usuario")
print (create_user('uservaleska2', 'senha', 'nomevaleska'))
print ("3: criar usuario")
print (create_user('uservaleska3', 'senha', 'nomevaleska'))

print ("4: mostrar todos os usuarios")
conn = sqlite3.connect('../user.db')
c = conn.cursor()
c.execute("select * from user")
print (c.fetchall())
print ("5: buscar usuario uservaleska")
print (get_user_by_username('uservaleska'))       

'''                 
