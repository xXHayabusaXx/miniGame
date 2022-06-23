from flask import Flask, request, redirect, session

import sys
sys.path.insert(1, 'OnePiece/workspace/python-pipeline/')
import menu as m

app = Flask(__name__)

sessionManager=SessionManager()
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
            user_input = [request.form["username"], request.form["password"]]
            session['username']=request.form["username"]
            return sessionManager.session(request.form["username"]).showMenu(user_input)
        #return menu.showMenu(user_input)


@app.route("/login/", methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return menu.showLogin("")
    if request.method == 'POST':
        return redirect("/")


@app.route("/clean/", methods=['GET','POST'])
def clean():
    menu.clean()
    return redirect('/login/')


@app.route("/bdd/", methods=['GET'])
def bdd():
    return menu.showBDD()


    	


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True, use_reloader=False)
    
  
  
class SessionManager(object):
    
    
    def __init__(self):
        self._playersID={}
        self._menusID={}
        
    def newSession(self, username):
        newid=self.maxID()+1
        self._playersID[username]=newid
        self._menusID[newid]=m.Menu()
        return self._menusID[newid]
        
        
    def session(self, username):
        if username in self._playersID:
            return self.getMenu(username)
        else:
            return self.newSession(username)
        
    def getMenu(self, username):
        return self._menusID[self._playersID[username]]
    
    
    def maxID():
        return max(self._playersID.values())
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
