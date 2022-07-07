from flask import Flask, request, redirect, session, render_template, url_for
from flask_login import LoginManager
from urllib.parse import urlparse, urljoin

import pathlib
print(pathlib.Path(__file__).parent.resolve())


import sys
sys.path.insert(1, 'OnePiece/workspace/python-pipeline/')

#import sessionManager as sm
from interactBDD import InteractBDD
from user import User

from forms import LoginForm
from forms import IndexForm

login_manager = LoginManager()

app = Flask(__name__)
#SESSION_TYPE='redis'
#app.config.from_object(__name__)
app.secret_key = 'fklessecretKeys12344321'

#sessionManager=sm.SessionManager()

login_manager.init_app(app)

@app.route("/", methods=['GET','POST'])
@login_required
def Menu():

    if request.method == 'GET':
        return redirect('/login/')
    if request.method == 'POST':
        if "user_input" in request.form:
            user_input = request.form["user_input"]
        

        output = current_user.menu.showMenu()
        return render_template('index.html', output=output, form=IndexForm())

        # TODO warn the password was wrong     
        
            
@app.errorhandler(404)
def page_not_found(error):
    return redirect('/login/')  


@app.route("/login/", methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # Login and validate the user.
        user = login()
        # user should be an instance of your `User` class
        login_user(user)

        flask.flash('Logged in successfully.')

        next = flask.request.args.get('next')
        # is_safe_url should check if the url is safe for redirects.
        # See http://flask.pocoo.org/snippets/62/ for an example.
        if not is_safe_url(next):
            return flask.abort(400)

        return flask.redirect(next or flask.url_for('index'))
    return flask.render_template('login.html', form=form)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect('login.html')

@app.route("/clean/", methods=['GET','POST'])
def clean():
    InteractBDD.deleteAll()
    return redirect('/login/')


@app.route("/bdd/", methods=['GET'])
def bdd():
    return InteractBDD.retrieveWholeDatabase()


def login():
    user = User()
    if "username" in request.form:
        username = request.form["username"]
        password = request.form["password"]
        user.checkPassword(username, password)
    return user

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)   

def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and \
           ref_url.netloc == test_url.netloc

def get_redirect_target():
    for target in request.values.get('next'), request.referrer:
        if not target:
            continue
        if is_safe_url(target):
            return target	

def redirect_back(endpoint, **values):
    target = request.form['next']
    if not target or not is_safe_url(target):
        target = url_for(endpoint, **values)
    return redirect(target)




if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True, use_reloader=False)
    