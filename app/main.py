from flask import Flask, request, redirect, session, render_template, url_for, flash
from flask_login import LoginManager,  login_required, current_user
from urllib.parse import urlparse, urljoin
from flask_wtf import FlaskForm

import pathlib
print(pathlib.Path(__file__).parent.resolve())


import sys
sys.path.insert(1, 'OnePiece/workspace/python-pipeline/')

from interactBDD import InteractBDD
from user import User#, Anonymous

from forms import LoginForm
from forms import IndexForm

login_manager = LoginManager()
login_manager.anonymous_user = User #Anonymous
login_manager.current_user = User
login_manager.login_view = "login"

app = Flask(__name__)
#SESSION_TYPE='redis'
#app.config.from_object(__name__)
app.secret_key = 'secretKeys12344321'


login_manager.init_app(app)

# TODO https://developer.mozilla.org/docs/Web/HTTP/Headers/Set-Cookie/SameSite


@app.route("/", methods=['GET','POST'])
def index():
    if "username" in request.form:
        username = request.form["username"]
        password = request.form["password"]

        # Login and validate the user.
        user = User(username)

        # user should be an instance of your `User` class
        login_user(user)
        current_user.checkPassword(username, password)

    if current_user.is_authenticated:
        return redirect(url_for('menu', username=current_user.username))
    else:
        return redirect(url_for('login'))
            
  
 
@app.route("/menu/<username>", methods=['GET','POST'])
@login_required
def menu(username=None): 
    form=IndexForm()
    if form.validate_on_submit():
        user_input = request.form["user_input"]
        output = current_user.menu.showMenu(user_input)
        return render_template('index.html', output=output, form=IndexForm(), username=username)
    
    output = current_user.menu.showMenu()
    return render_template('index.html', output=output, form=IndexForm(), username=username)
    
    


            
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
        return redirect(url_for('index'))
    
    return render_template('login.html', form=form)

@app.route("/logout")
@login_required
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
    