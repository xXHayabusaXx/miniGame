from flask import Flask, request, redirect, render_template, url_for, flash
from flask_login import LoginManager,  login_required, current_user, login_user, logout_user
from urllib.parse import urlparse, urljoin

import pathlib
print(pathlib.Path(__file__).parent.resolve())


import sys
sys.path.insert(1, 'OnePiece/workspace/python-pipeline/')

from interactBDD import InteractBDD
from user import User, Anonymous
from utils import Utils

from forms import LoginForm
from forms import IndexForm

login_manager = LoginManager()
login_manager.anonymous_user = Anonymous
login_manager.current_user = User
login_manager.login_view = "login"

app = Flask(__name__)
app.secret_key = 'secretKeys12344321'
app.add_url_rule("/", endpoint="login")

login_manager.init_app(app)

user_input=None

# TODO https://developer.mozilla.org/docs/Web/HTTP/Headers/Set-Cookie/SameSite

      
     
@app.before_request
def handle_request():
    global user_input
    if "user_input" in request.form:
        user_input = request.form["user_input"]

    elif "username" in request.form:
        username = request.form["username"]
        password = request.form["password"]
        checkPassword(username, password)

  
 
@app.route("/menu/<username>", methods=['GET','POST'])
def menu(username=None): 
    if current_user.is_authenticated:
        form=IndexForm()
        if form.validate_on_submit():
            return redirect(url_for('menu'))
        
        global user_input
        output = current_user.menu.showMenu(user_input)
        return render_template('index.html', output=output, form=IndexForm(), username=username)
    return redirect(url_for("login"))

def checkPassword(username, password):
    if Utils.sanitization([username, password]):
        password=Utils.hashPassword(password)
        if InteractBDD.existInDB(username):
            if not InteractBDD.checkPassword(username, password):
                return False
            else:
                user = User(username)
                login_user(user, remember=True)
                return True
        
        user = User(username, password)
        login_user(user)
        return True

            
@app.errorhandler(404)
def page_not_found(error):
    return redirect(url_for('login'))


@app.route("/login/", methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        '''next = request.args.get('index')
        request.forms['next'] = next
        if not is_safe_url(next):
            return abort(400)

        return redirect(next or url_for('index'))'''
        return redirect(url_for('menu'))
    
    return render_template('login.html', form=form)


@app.route("/logout")
def logout():
    logout_user()
    flash("You've been logged out! Come back soon!", "success")
    return redirect(url_for('login'))

@app.route("/clean/", methods=['GET','POST'])
def clean():
    InteractBDD.deleteAll()
    return redirect('/login/')


@app.route("/bdd/", methods=['GET'])
def bdd():
    return InteractBDD.retrieveWholeDatabase()


@login_manager.user_loader
def load_user(id):
    username = InteractBDD.getUsername(id)
    user = User(username)
    return user


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
    