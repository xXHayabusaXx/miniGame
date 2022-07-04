from flask import Flask, request, redirect, session, render_template

import pathlib
print(pathlib.Path(__file__).parent.resolve())


import sys
sys.path.insert(1, 'OnePiece/workspace/python-pipeline/')
import menu as m
import sessionManager as sm
import interactBDD as bdd
from forms import LoginForm
from forms import IndexForm

app = Flask(__name__)
SESSION_TYPE='redis'
app.config.from_object(__name__)
app.secret_key = 'secretKey'

sessionManager=sm.SessionManager()

@app.route("/", methods=['GET','POST'])
def Menu():

    if request.method == 'GET':
        return redirect('/login/')
    if request.method == 'POST':
        if "user_input" in request.form:
            user_input = request.form["user_input"]
        elif "username" in request.form:
            user_input = [request.form["username"], request.form["password"]]
            session['username']=request.form["username"]
        else:
            return "Bad request error"

        [output, auth]=sessionManager.session(session.get('username'), session.get('auth'), user_input)
        if auth:
            session['auth']=True
            return render_template('index.html', output=output, form=IndexForm())
        else:
            return redirect('/login/')
            # TODO warn the password was wrong     
        
            
@app.errorhandler(404)
def page_not_found(error):
    return redirect('/login/')  


@app.route("/login/", methods=['GET','POST'])
def login():
    session['auth']=False
    session['username']=None
    if request.method == 'GET':
        formulaire = LoginForm()
        return render_template('login.html', form=formulaire)
    if request.method == 'POST':
        return redirect("/")


@app.route("/clean/", methods=['GET','POST'])
def clean():
    bdd.deleteAll()
    return redirect('/login/')


@app.route("/bdd/", methods=['GET'])
def bdd():
    return bdd.retrieveWholeDatabase()


    	


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True, use_reloader=False)
    