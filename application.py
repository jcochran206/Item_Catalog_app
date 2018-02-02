from flask import Flask, render_template, request, redirect,jsonify, url_for, flash
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setupVG import GameCategory, Base, GameItem
app = Flask(__name__)

#connect to database videogames
engine = create_engine('sqlite:///videogames.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

@app.route('/')
@app.route('/index')
def home():
	return "hello index"
# return api calls here 
# show all categories
@app.route('/Category/JSON')
def categoryJSON():
	categories = session.query(GameCategory).all()
	return jsonify(categories=[i.serialize for i in categories])

#show all items by categories
@app.route('/category/<int:category_id>/game/JSON')
def gameItemJSON(category_id):
	categories = session.query(GameCategory).filter_by(id = category_id).one()
	items = session.query(GameItem).filter_by(category_id=category_id).all()
	return jsonify(GameItem=[i.serialize for i in items])

#show game items 
@app.route('/category/<int:category_id>/menu/<int:gameitem_id>/JSON')
def categoryGamesJSON(category_id, gameitem_id):
	game_item = session.query(GameItem).filter_by(id=gameitem_id).one()
	return jsonify(game_item = game_item.serialize)


#show all categories
@app.route('/category/')
def showCategories():
	categories = session.query(GameCategory).first()
	items = session.query(GameItem).filter_by(category_id=categories.id)
	# output = ''
	# for i in items:
	# 	output += i.name
	#  	output += '</br>'
	#  	output += i.price
	#  	output += '</br>'
	#  	output += i.description
	#  	output += '</br>'
	# return output
	#return render_template('main.html', category_id = categories.id)
# Game Menu Item

@app.route('/category/<int:category_id>/')
def categoryGame(category_id):
	categories = session.query(GameCategory).filter_by(id=category_id).one()
	items = session.query(GameItem).filter_by(category_id=categories.id)
	return render_template('main.html', categories=categories, items=items)
#NEW CATEGORY
@app.route('/category/<int:category_id>/new/', methods=['GET', 'POST'])
def newGameItem(category_id):
	if request.method == 'POST':
		newItem = GameItem(name = request.form['name'],category_id=category_id)
		session.add(newItem)
		session.commit()
		return redirect(url_for('showCategories', category_id=category_id))
	else:
		return render_template('newgameitem.html', category_id=category_id)

#Edit Category here
@app.route('/category/<int:category_id>/<int:game_item_id>/edit/', methods=['GET','POST'])
def editCategory(category_id, game_item_id):
	editedItem = session.query(GameItem).filter_by(id=game_item_id).one()
	if request.method == 'POST':
		if request.form['name']:
			editedItem.name = request.form['name']
		session.add(editedItem)
		session.commit()
		return redirect(url_for('showCategories', category_id=category_id))
	else:
		return render_template('editgameitem.html', category_id=category_id, game_item_id=game_item_id, item=editedItem)

	return 'edit materials go here'

#delete Category here
@app.route('/category/<int:category_id>/delete/', methods=['GET','POST'])
def deleteCategory(category_id):
	return 'delete materials go here'



if __name__ == '__main__':
	app.debug = True
	app.run(host = '0.0.0.0', port=8000)