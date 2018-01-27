from flask import Flask, render_template, request, redirect,jsonify, url_for, flash
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setupVG import GameCategory, Base, GameItem
app = Flask(__name__)

engine = create_engine('sqlite:///videogames.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

@app.route('/')
@app.route('/index')
def home():
	return "hello index"

@app.route('/Category/JSON')
def categoryJSON():
	#return all categories
	categories = session.query(GameCategory).all()
	return jsonify(categories=[i.serialize for i in categories])

#show all categories
@app.route('/category/')
def showCategories():
	categories = session.query(GameCategory).first()
	items = session.query(GameItem).filter_by(game_id=categories.id)
	output = ''
	for i in items:
		output += i.name
	 	output += '</br>'
	 	output += i.price
	 	output += '</br>'
	 	output += i.description
	 	output += '</br>'
	return output
	#return render_template('main.html', game_id = GameCategory.id)

#NEW CATEGORY
@app.route('/categories/new/', methods=['GET', 'POST'])
def newCategory():
	return 'New item here'

#Edit Category here
@app.route('/categories/<int:game_id>/edit/', methods=['GET','POST'])
def editCategory(game_id):
	return 'edit materials go here'



if __name__ == '__main__':
	app.debug = True
	app.run(host = '0.0.0.0', port=8000)