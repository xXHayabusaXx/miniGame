from tkinter import E
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

login_manager.init_app(app)


# TODO https://developer.mozilla.org/docs/Web/HTTP/Headers/Set-Cookie/SameSite



@app.route("/menu/<username>", methods=['GET','POST'])
@login_required
def menu(username=None, user_input=None): 
    form=IndexForm()
    if form.validate_on_submit():
        user_input=form.user_input
        return redirect(url_for('menu', username=current_user.username, user_input=user_input))
        
    output = current_user.menu.showMenu(user_input)
    return render_template('index.html', output=output, form=IndexForm(), username=username)
    

def checkPassword(username, password):
    if Utils.sanitization([username, password]):
        password=Utils.hashPassword(password)
        if InteractBDD.existInDB(username):
            if not InteractBDD.checkPassword(username, password):
                return False
            else:
                user = User(username)
                login_user(user)
                return True
        
        user = User(username, password)
        login_user(user)
        return True

            
@app.errorhandler(404)
def page_not_found(error):
    return redirect(url_for('login'))


@app.route("/login/", methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username=request.form['username']
        password=request.form['password']
        checkPassword(username, password)
    else:
        if current_user.is_authenticated:
            user_input=None
            if "user_input" in request.form:
                user_input= request.form["user_input"]
            return redirect(url_for('menu', username=current_user.username, user_input=user_input))


        form = LoginForm()
        return render_template('login.html', form=form)


@app.route("/logout")
def logout():
    logout_user()
    flash("You've been logged out! Come back soon!", "success")
    return redirect(url_for('login'))

@app.route("/clean/", methods=['GET','POST'])
def clean():
    InteractBDD.deleteAll()
    return redirect(url_for('login'))


@app.route("/bdd/", methods=['GET'])
def bdd():
    return InteractBDD.retrieveWholeDatabase()


@login_manager.user_loader
def load_user(id):
    username = InteractBDD.getUsername(id)
    user = User(username)
    return user





if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True, use_reloader=False)
    