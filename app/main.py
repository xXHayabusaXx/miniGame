from flask import Flask, request, redirect

import sys
sys.path.insert(1, 'OnePiece/')
import menu as m

app = Flask(__name__)

menu = m.Menu()

@app.route("/", methods=['GET','POST'])
def Menu():
    if request.method == 'GET':
        return menu.showMenu("")
    if request.method == 'POST':
        user_input = request.form["user_input"]
        return menu.showMenu(user_input)


@app.route("/clean", methods=['GET','POST'])
def clean():
    m.Menu().clean()
    return redirect('/')




if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)#, use_reloader=False)
