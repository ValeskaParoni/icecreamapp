from settings.config_app import generate_password_hash, check_password_hash, db, app

class LoginException(Exception):
    def __init__(self, error):
        self.error = error
    def msg(self):
        return self.error

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True)
    name = db.Column(db.String(100), unique=False)
    pw_hash = db.Column(db.String(300), unique=False)
    email = db.Column(db.String(100), unique=True)

    def __init__(self, username, password_hash, name, email):
        self.username = username
        self.pw_hash = password_hash
        self.name = name
        self.email = email

    def check_password(self, password):
        return check_password_hash(self.pw_hash, password)

    def _get_name(self):
        return self.name

    def _get_username(self):
        return self.username

    def print_email(self):
        print(self.email)

    def change_password(self, new_unhashed_password):
        self.pw_hash = generate_password_hash(new_unhashed_password)
        db.session.commit()


    @staticmethod
    def user_exists(username):
        users = User.query.filter_by(username=username)
        return users.first()

    @staticmethod
    def create_user(username, unhashed_password, name, email):
        if not User.user_exists(username):
            db.session.add(User(username, generate_password_hash(unhashed_password), name, email))
            db.session.commit()
            return True
        raise LoginException('username_exists')

    @staticmethod
    def find_email(email):
        user = User.query.filter_by(email=email).first()
        if user:
            return user
        else:
            raise LoginException('wrong_email')

    @staticmethod
    def check_user_and_password(username, unhashed_password):
        user = User.user_exists(username)
        if user:
            if user.check_password(unhashed_password):
                return user 
            raise LoginException('wrong_password')
        raise LoginException('wrong_username')

    @staticmethod
    def get_name(username):
        user = user_exists(username)
        try:
            return user._get_name()
        except Exception as a:
            print (a)
            return False
