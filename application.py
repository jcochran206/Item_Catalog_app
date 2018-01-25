from flask import Flask, jsonify
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
@app.route('/categories/')
def showCategories():
	categories = session.query(category).order_by(asc(category.name))
	return "get out put here to render"

#NEW CATEGORY
@app.route('/categories/new/', methods=['GET', 'POST'])
def newCategory():
	return 'New item here'

#Edit Category here
@app.route('/categories/<int:category_id>/edit/', methods=['GET','POST'])
def editCategory(category_id):
	return 'edit materials go here'



if __name__ == '__main__':
	app.debug = True
	app.run(host = '0.0.0.0', port=8000)