from flask import session, request, render_template, redirect
from auth_v2 import User, app, LoginException


@app.route('/login', methods=["GET"])
def login_page(error=False):
    if 'logged_in' in session:
        return redirect('/home')
    print(error)
    return render_template('login_page.txt', login_post_url = '/login', create_account_url = '/newaccount', error=error, forgot_password_url ='/forgotpassword')

@app.route('/login', methods=["POST"])
def check_login():
    try:
        user = User.check_user_and_password(request.form['username'], request.form['pass'])
    except LoginException as e:
        return login_page(e.error)
    session['logged_in'] = user._get_username()
    session['name'] = user._get_name()
    return redirect('/home')

@app.route('/forgotpassword', methods=['GET'])
def forgot_password_page(error=False):
    if 'logged_in' in session:
        return redirect('/home')
    return render_template('forgot_password_form_page.txt', forgot_password_url = '/forgotpassword', error=error, create_account_url='/newaccount')

@app.route('/forgotpassword', methods=['POST'])
def send_email_to_recover_password():
    try:
        user = User.find_email(request.form['email'])
        user.print_email()
        return render_template('email_sent.txt', send_email_url='forgotpassword', email=request.form['email'])
    except LoginException as e:
        return forgot_password_page(e.error)

@app.route('/changepassword', methods=["GET"])
def ask_for_new_password(error=False):
    if 'logged_in' in session:
        return render_template('change_password_logged.txt', new_password_url='/changepassword', error=error)
    else:
        return redirect('/home')

@app.route('/changepassword', methods["POST"])
def change_password

@app.route('/newaccount', methods=["GET"])
def render_new_account_page():
    if 'logged_in' in session:
        return redirect('/home')
    return render_template('new_account_form.txt', create_account_post_url = '/newaccount', username_error = False)

@app.route('/newaccount', methods=["POST"])
def create_new_account():
    if User.create_user(request.form['username'], request.form['pass'], request.form['name'], request.form['email']):
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
