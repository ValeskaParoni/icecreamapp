from views import account_views, login_views, other_views
from settings.config_app import app, redirect

@app.route('/')
def default():
    return redirect('/home')

if __name__ == '__main__':
    app.run()
