from flask import Flask, request, redirect, session, render_template, url_for
from flask_login import LoginManager,  login_required, current_user
from urllib.parse import urlparse, urljoin
from flask_wtf import FlaskForm

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
app.secret_key = 'secretKeys12344321'

#sessionManager=sm.SessionManager()

login_manager.init_app(app)




@app.route("/<username>", methods=['GET','POST'])
@app.route("/", methods=['GET','POST'])
def index(username=None):
    try:
        username=current_user.menu.username
    except:
        username=None

    if username==None:
        if current_user.is_authenticated:
            redirect(url_for('index', username=username))
        else:
            redirect(url_for('login'))
            
    if current_user.is_authenticated:
        form=IndexForm()
        if form.validate_on_submit():
            if "user_input" in request.form:
                user_input = request.form["user_input"]
                output = current_user.menu.showMenu(user_input)
            else:
                output = current_user.menu.showMenu()
            return render_template('index.html', output=output, form=IndexForm(), username=username)
    
        return render_template('index.html', output=current_user.menu.showMenu(), form=IndexForm(), username=username)
    return redirect(url_for('login'))
    


            
@app.errorhandler(404)
def page_not_found(error):
    return redirect(url_for('login'))


@app.route("/login/", methods=['GET','POST'])
def login():
    
    form = LoginForm()
    if form.validate_on_submit():
        # Login and validate the user.
        current_user = login(form)

        if current_user.is_authenticated:
            # user should be an instance of your `User` class
            login_user(current_user)

            next = request.args.get('index')
            request.forms['next'] = next
            if not is_safe_url(next):
                return abort(400)

            return redirect(next or url_for('index'))
        else:
            flash("Your password doesn't match!", "error")
    
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


def login(form):
    user = User()
    if "username" in form:
        username = form["username"]
        password = form["password"]
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
    