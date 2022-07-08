from flask import Flask, request, redirect, session, render_template, url_for, flash
from flask_login import LoginManager,  login_required, current_user
from urllib.parse import urlparse, urljoin
from flask_wtf import FlaskForm

import pathlib
print(pathlib.Path(__file__).parent.resolve())


import sys
sys.path.insert(1, 'OnePiece/workspace/python-pipeline/')

from interactBDD import InteractBDD
from user import User

from forms import LoginForm
from forms import IndexForm

login_manager = LoginManager()

app = Flask(__name__)
#SESSION_TYPE='redis'
#app.config.from_object(__name__)
app.secret_key = 'secretKeys12344321'


login_manager.init_app(app)

# TODO https://developer.mozilla.org/docs/Web/HTTP/Headers/Set-Cookie/SameSite


@app.route("/<username>", methods=['GET','POST'])
@app.route("/", methods=['GET','POST'])
def index(username=None):
    try:
        username=current_user.menu.username
    except:
        return redirect(url_for('login'))

    if username==None and current_user.is_authenticated:
        redirect(url_for('index', username=username))
            
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
@app.route("/login/<variable>", methods=['GET','POST'])
def login(variable=None):
    
    form = LoginForm()
    if form.validate_on_submit():
        # Login and validate the user.
        user = User()
        username = form.username.data
        password = form.password.data
        user.checkPassword(username, password)

        # user should be an instance of your `User` class
        login_user(user)

        #if current_user.is_authenticated:

        #    next = request.args.get('index')
        #    request.forms['next'] = next
        #    if not is_safe_url(next):
        #        return abort(400)

        #return redirect(next or url_for('index'))
        return redirect(url_for('index', variable=username))
        #else:
        #    flash("Your password doesn't match!", "error")
    else:
        flash("Ton identifiant/password doit faire entre 4 et 20 caractères", "error")
    
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
    # 1. Fetch against the database a user by `id` 
    # 2. Create a new object of `User` class and return it.
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
    