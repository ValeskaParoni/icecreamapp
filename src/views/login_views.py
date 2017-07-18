from settings.config_app import app, session, redirect, render_template, request
from utils.auth import User, LoginException

@app.route('/login', methods=["GET"])
def login_page(error=False):
    if 'logged_in' in session:
        return redirect('/home')
    print(error)
    return render_template('login_page.html', send_to = '/login', create_account_url = '/createaccount', error=error, forgot_password_url ='/forgotpassword')

@app.route('/login', methods=["POST"])
def check_login():
    try:
        user = User.check_user_and_password(request.form['username'], request.form['password'])
    except LoginException as e:
        return login_page(e.error)
    session['logged_in'] = user._get_username()
    session['name'] = user._get_name()
    return redirect('/home')

@app.route('/logout')
def logout():
    if 'logged_in' in session:
        session.pop('logged_in')
    if 'name' in session:
        session.pop('name')
    return redirect('/login')
