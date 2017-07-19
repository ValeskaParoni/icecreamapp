from config_app import app, session, redirect, render_template, request
from utils.auth import User, LoginException

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

