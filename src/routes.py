from flask import Flask, session, request, render_template, redirect
from flask_sqlalchemy import SQLAlchemy
import auth_v2

app = Flask(__name__)
app.secret_key = '34whiufgiug8342'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////user.db'
db = SQLAlchemy(app)


@app.route('/login', methods=["GET"])
def login_page():
    if 'logged_in' in session:
        return redirect('/home')
    return render_template('login_page.txt', login_post_url = '/login', create_account_url = '/newaccount', username_error = auth.errors['username'], password_error = auth.errors['password'])

@app.route('/login', methods=["POST"])
def check_login():
    if (auth.check_user(request.form['username'], request.form['pass'])):
        session['logged_in'] = True
        session['name'] = auth.get_name(request.form['username'])
        return redirect('/home')
    return redirect('/login')





@app.route('/newaccount', methods=["GET"])
def render_new_account_page():
    if 'logged_in' in session:
        return redirect('/home')
    return render_template('new_account_form.txt', create_account_post_url = '/newaccount', username_error = auth.errors['username'])

@app.route('/newaccount', methods=["POST"])
def create_new_account():
    if auth.new_user(request.form['username'], request.form['pass'], request.form['name']):
        return redirect('/login', code = 307)
    return redirect('/newaccount')





@app.route('/logout')
def logout():
    if 'logged_in' in session:
        session.pop('logged_in')
    if 'name' in session:
        session.pop('name')
    return redirect('/login')





@app.route('/home')
def home_page():
    if 'logged_in' in session:
        return render_template('home_page.txt', name = session['name'], logout_url = '/logout')
    return redirect('/login')

@app.route('/')
def default():
    return redirect('/home')


if __name__ == '__main__':
    app.run()
