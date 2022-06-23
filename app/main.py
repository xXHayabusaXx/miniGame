from flask import Flask, request, redirect

import sys
sys.path.insert(1, 'OnePiece/workspace/python-pipeline/')
"""
import menu as m

app = Flask(__name__)

menu = m.Menu()

@app.route("/", methods=['GET','POST'])
def Menu():
    if request.method == 'GET':
        return redirect('/login/')
    if request.method == 'POST':
        try:
            user_input = request.form["user_input"]
        except:
            user_input = [request.form["username"], request.form["password"]]
        return menu.showMenu(user_input)


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
    
"""    
    
    
    
    
    
