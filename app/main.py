from flask import Flask, request, redirect, session, render_template

import pathlib
print(pathlib.Path(__file__).parent.resolve())


import sys
sys.path.insert(1, 'OnePiece/workspace/python-pipeline/')
import menu as m
import sessionManager as sm


app = Flask(__name__)#, static_url_path='/app', static_folder='static') #, template_folder='templates'
SESSION_TYPE='redis'
app.config.from_object(__name__)
app.secret_key = 'secretKey'

sessionManager=sm.SessionManager()

@app.route("/", methods=['GET','POST'])
def Menu():

    if request.method == 'GET':
        return redirect('/login/')
    if request.method == 'POST':
        try:
            user_input = request.form["user_input"]
            if 'username' in session:
            	return sessionManager.session(session.get('username')).showMenu(user_input)
            else:
            	return "Go to login page"
            
        except:
            user_input = [request.form["username"], request.form["password"]]
            session['username']=request.form["username"]
            return sessionManager.session(request.form["username"]).showMenu(user_input)
            
@app.errorhandler(404)
def page_not_found(error):
    return redirect('/login/')  


@app.route("/login/", methods=['GET','POST'])
def login():
    if request.method == 'GET':
        #return m.Menu().showLogin("")
        return render_template('login.html')
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
    
