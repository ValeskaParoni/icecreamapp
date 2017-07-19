from config_app import app, session, redirect, render_template

@app.route('/home')
def home_page():
    if 'logged_in' in session:
        return render_template('home_page.html', name = session['name'], logout_url = '/logout', change_password_url='/changepassword')
    return redirect('/login')

