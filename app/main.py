from flask import Flask, request, redirect, session

import sys
sys.path.insert(1, 'OnePiece/workspace/python-pipeline/')
import menu as m
import sessionManager as sm


app = Flask(__name__)
SESSION_TYPE='redis'
app.config.from_object(__name__)
app.secret_key = 'secretKey'

sessionManager=sm.SessionManager()
#menu = m.Menu()

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
        
            try:
                user_input = [request.form["username"], request.form["password"]]
                session['username']=request.form["username"]
                return sessionManager.session(request.form["username"]).showMenu(user_input)
            except:
                return redirect('/login/')
        #return menu.showMenu(user_input)


@app.route("/login/", methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return m.Menu().showLogin("")
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
    
  

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
