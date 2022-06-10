from flask import Flask, request

import sys
sys.path.insert(1, 'OnePiece/')
import menu as m

app = Flask(__name__)

@app.route("/", methods=['GET','POST'])
def Menu():
	if request.method == 'GET':
        	return m.Menu().showMenu("")
    	if request.method == 'POST':
        	user_input = request.form("user_input")
        	return return m.Menu().showMenu(user_input)
	#return m.Menu().showMenu()

if __name__ == "__main__":
	app.run(host='0.0.0.0', port=8080, debug=True, use_reloader=False)
