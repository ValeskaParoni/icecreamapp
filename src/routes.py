from flask import session, request, render_template, redirect
from auth_v2 import User, app, LoginException


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

@app.route('/forgotpassword', methods=["GET"])
def forgot_password_page(error=False):
    if 'logged_in' in session:
        return redirect('/home')
    return render_template('forgot_password_page.html', send_to = '/forgotpassword', error=error, create_account_url='/createaccount')

@app.route('/forgotpassword', methods=["POST"])
def send_email_to_recover_password():
    try:
        user = User.find_email(request.form['email'])
        user.print_email()
        return render_template('email_sent_page.html', send_to='/forgotpassword', email=request.form['email'])
    except LoginException as e:
        return forgot_password_page(e.error)

@app.route('/changepassword', methods=["GET"])
def ask_for_new_password(error=False):
    if 'logged_in' in session:
        return render_template('change_password_page.html', send_to='/changepassword', error=error)
    else:
        return redirect('/home')

@app.route('/changepassword', methods=["POST"])
def change_password():
    if 'logged_in' in session:
        username = session['logged_in']
        password = request.form['old_password']
        new_password = request.form['new_password']
        try:
            user = User.check_user_and_password(username, password)
            user.change_password(new_password)
            return render_template('password_changed_page.html', home='/home')
        except LoginException as e:
            return ask_for_new_password(e.error) 

@app.route('/createaccount', methods=["GET"])
def render_new_account_page(error=False):
    if 'logged_in' in session:
        return redirect('/home')
    return render_template('create_account_page.html', send_to = '/createaccount', error=error, login_url='/login')

@app.route('/createaccount', methods=["POST"])
def create_new_account():
    try:
        User.create_user(request.form['username'], request.form['password'], request.form['name'], request.form['email'])
        return redirect('/login', code='307')
    except LoginException as e:
        return render_new_account_page(e.error)

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
        return render_template('home_page.html', name = session['name'], logout_url = '/logout', change_password_url='/changepassword')
    return redirect('/login')

@app.route('/')
def default():
    return redirect('/home')


if __name__ == '__main__':
    app.run()
