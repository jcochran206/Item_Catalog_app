from flask import Flask
app = Flask(__name__)

@app.route('/')
@app.route('/index')
def home():
	return "hello index"

if __name__ == '__main__':
	app.debug = True
	app.run(localhost = '0.0.0.0', port=8000)