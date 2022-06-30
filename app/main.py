from flask import Flask, request, redirect, session, render_template

import pathlib
print(pathlib.Path(__file__).parent.resolve())


import sys
sys.path.insert(1, 'OnePiece/workspace/python-pipeline/')
import menu as m
import sessionManager as sm
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
        if "user_input" in request.form and "username" in session:
            user_input = request.form["user_input"]
        elif "username" in request.form:
            user_input = [request.form["username"], request.form["password"]]
            session['username']=request.form["username"]
        else:
            return "Bad request error"

        output=sessionManager.session(session.get('username')).showMenu(user_input)
        #return sessionManager.session(session.get('username')).showMenu(user_input)
        formulaire= IndexForm()
        return render_template('index.html', map=output['map'], content=output['content'], team=output['team'], form=formulaire)
        
        
            
@app.errorhandler(404)
def page_not_found(error):
    return redirect('/login/')  


@app.route("/login/", methods=['GET','POST'])
def login():
    if request.method == 'GET':
        formulaire = LoginForm()
        return render_template('login.html', form=formulaire)
    if request.method == 'POST':
        return redirect("/")


@app.route("/clean/", methods=['GET','POST'])
def clean():
    m.Menu.clean()
    return redirect('/login/')


@app.route("/bdd/", methods=['GET'])
def bdd():
    return m.Menu().showBDD()


    	


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True, use_reloader=False)
    