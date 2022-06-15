from flask import Flask, request, redirect

import sys
sys.path.insert(1, 'OnePiece/')
import menu as m

app = Flask(__name__)

menu = m.Menu()

@app.route("/", methods=['GET','POST'])
def Menu():
    if request.method == 'GET':
        return redirect('/login')
    if request.method == 'POST':
        username = request.form["username"]
        password = request.form["password"]
        return menu.sendCredentials(username, password)


@app.route("/login/", methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return menu.showLogin()
    if request.method == 'POST':
        user_input = request.form["user_input"]
        redirect('/')
        return menu.showMenu("user_input")


@app.route("/clean/", methods=['GET','POST'])
def clean():
    menu.clean()
    return redirect('/')



if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True, use_reloader=False)
