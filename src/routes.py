from flask import session, request, render_template, redirect
from auth_v2 import User, app, LoginException


@app.route('/login', methods=["GET"])
def login_page(error=False):
    if 'logged_in' in session:
        return redirect('/home')
    print(error)
    return render_template('login_page.txt', login_post_url = '/login', create_account_url = '/newaccount', error=error)

@app.route('/login', methods=["POST"])
def check_login():
    try:
        user = User.check_user_and_password(request.form['username'], request.form['pass'])
        session['logged_in'] = True
        session['name'] = user._get_name()
        return redirect('/home')
    except LoginException as e:
        return login_page(e.error)





@app.route('/newaccount', methods=["GET"])
def render_new_account_page():
    if 'logged_in' in session:
        return redirect('/home')
    return render_template('new_account_form.txt', create_account_post_url = '/newaccount', username_error = False)

@app.route('/newaccount', methods=["POST"])
def create_new_account():
    if User.create_user(request.form['username'], request.form['pass'], request.form['name']):
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
