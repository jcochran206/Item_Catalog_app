from flask import Flask, render_template, request, redirect,jsonify, url_for, flash
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from database_setupVG import GameCategory, Base, GameItem

#imports for antiforgery
from flask import session as login_session
import random
import string

#imports Oauth requirements
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests 


app = Flask(__name__)

#connect to database
engine = create_engine('sqlite:///videogames.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

#route to login page 
@app.route('/login/')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(32))
    login_session['state'] = state
    return render_template('login.html', STATE=state)

#fbconnect
@app.route('/fbconnect', methods=['POST'])
def fbconnect():
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    access_token = request.data
    print "access token received %s " % access_token


    app_id = json.loads(open('fb_client_secrets.json', 'r').read())[
        'web']['app_id']
    app_secret = json.loads(
        open('fb_client_secrets.json', 'r').read())['web']['app_secret']
    url = 'https://graph.facebook.com/oauth/access_token?grant_type=fb_exchange_token&client_id=%s&client_secret=%s&fb_exchange_token=%s' % (
        app_id, app_secret, access_token)
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]


    # Use token to get user info from API
    userinfo_url = "https://graph.facebook.com/v2.8/me"
    '''
        Due to the formatting for the result from the server token exchange we have to
        split the token first on commas and select the first index which gives us the key : value
        for the server access token then we split it on colons to pull out the actual token value
        and replace the remaining quotes with nothing so that it can be used directly in the graph
        api calls
    '''
    token = result.split(',')[0].split(':')[1].replace('"', '')

    url = 'https://graph.facebook.com/v2.8/me?access_token=%s&fields=name,id,email' % token
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    # print "url sent for API access:%s"% url
    # print "API JSON result: %s" % result
    data = json.loads(result)
    login_session['provider'] = 'facebook'
    login_session['username'] = data["name"]
    login_session['email'] = data["email"]
    login_session['facebook_id'] = data["id"]

    # The token must be stored in the login_session in order to properly logout
    login_session['access_token'] = token

    # Get user picture
    url = 'https://graph.facebook.com/v2.8/me/picture?access_token=%s&redirect=0&height=200&width=200' % token
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    data = json.loads(result)

    login_session['picture'] = data["data"]["url"]

    # see if user exists
    # user_id = getUserID(login_session['email'])
    # if not user_id:
    #     user_id = createUser(login_session)
    # login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']

    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '

    flash("Now logged in as %s" % login_session['username'])
    return output


@app.route('/fbdisconnect')
def fbdisconnect():
    facebook_id = login_session['facebook_id']
    # The access token must me included to successfully logout
    access_token = login_session['access_token']
    url = 'https://graph.facebook.com/%s/permissions?access_token=%s' % (facebook_id,access_token)
    h = httplib2.Http()
    result = h.request(url, 'DELETE')[1]
    return "you have been logged out"

#return api calls
#return all categories
@app.route('/category/JSON')
def categoryJSON():
    categories = session.query(GameCategory).all()
    return jsonify(categories=[i.serialize for i in categories])

#return game items by category JSON
@app.route('/category/<int:category_id>/game/JSON')
def gameItemJSON(category_id):
    categories = session.query(GameCategory).filter_by(id = category_id).one()
    items = session.query(GameItem).filter_by(category_id=category_id).all()
    return jsonify(GameItem=[i.serialize for i in items])

#routing goes here
#show all categories
@app.route('/')
@app.route('/category/')
def showAllCategories():
    categories = session.query(GameCategory).order_by(asc(GameCategory.name))
    return render_template('videoGames.html', categories = categories)
#show games by categories
# @app.route('/category/<int:category_id>/')
# def gamesByCategory(category_id):
#   categories = session.query(GameCategory).filter_by(id=category_id).one()
#   items = session.query(GameItem).filter_by(category_id=categories.id)
#   return render_template('videoGames.html', categories=categories)

#create new category
@app.route('/category/new', methods=['GET', 'POST'])
def newVGCategory():
    if request.method == 'POST':
        newCategory = GameCategory(name = request.form['name'])
        session.add(newCategory)
        flash('New Video Game Category was successfully created %s' % newCategory.name)
        session.commit()
        return redirect(url_for('showAllCategories'))
    else:
        return render_template('newVGcategory.html')

#edit a category
@app.route('/category/<int:category_id>/edit/', methods = ['GET','POST'])
def editCategory(category_id):
    editedCategory = session.query(GameCategory).filter_by(id = category_id).one()
    if request.method == 'POST':
        if request.form['name']:
            editedCategory.name = request.form['name']
            flash('Category successfully Edited %s' % editedCategory.name)
            return redirect(url_for('showAllCategories'))
    else:
            return render_template('editCategory.html', category = editedCategory)

#delete a Category
@app.route('/category/<int:category_id>/delete/', methods = ['GET','POST'])
def deleteCategory(category_id):
    categoryToDelete = session.query(GameCategory).filter_by(id = category_id).one()
    if request.method == 'POST':
        session.delete(categoryToDelete)
        flash('%s Successfully Deleted' % categoryToDelete.name)
        session.commit()
        return redirect(url_for('showAllCategories', category_id = category_id))
    else:
        return render_template('deleteVGCategory.html', category = categoryToDelete)

#show Category of games
@app.route('/category/<int:category_id>/')
@app.route('/category/<int:category_id>/game/')
def showGameItems(category_id):
    categories = session.query(GameCategory).filter_by(id = category_id).one()
    items = session.query(GameItem).filter_by(category_id =category_id).all()
    return render_template('gameItems.html', items = items, categories = categories)

#create new game items
@app.route('/category/<int:category_id>/game/new', methods=['GET', 'POST'])
def newGameItem(category_id):
    categories = session.query(GameCategory).filter_by(id=category_id).one()
    if request.method == 'POST':
        newGameItem = GameItem(name = request.form['name'], description = request.form['description'], price = request.form['price'], systemType = request.form['systemType'], category_id = category_id)
        session.add(newGameItem)
        session.commit()
        flash('New Game %s Item Successfully Created' % newGameItem.name)
        return redirect(url_for('showGameItems', category_id = category_id))
    else:
        return render_template('newGameItem.html', category_id = category_id)

#edit a game item
@app.route('/category/<int:category_id>/game/<int:game_id>/edit', methods=['GET','POST'])
def editGameItem(category_id, game_id):
    editedGameItem = session.query(GameItem).filter_by(id=game_id).one()
    categories = session.query(GameCategory).filter_by(id=category_id).one()
    if request.method == 'POST':
        if request.form['name']:
            editedGameItem.name = request.form['name']
        if request.form['description']:
            editGameItem.description = request.form['description']
        if request.form['price']:
            editedGameItem.price = request.form['price']
        if request.form['systemType']:
            editedGameItem.systemType = request.form['systemType']
        session.add(editedGameItem)
        session.commit()
        flash('Game Item Successfully Edited')
        return redirect(url_for('showGameItems', category_id = category_id))
    else:
        return render_template('editGameItem.html', category_id=category_id, game_id=game_id, item=editedGameItem)

#delete a game item 
@app.route('/category/<int:category_id>/game/<int:game_id>/delete', methods=['GET','POST'])
def deleteGameItem(category_id, game_id):
    categories = session.query(GameCategory).filter_by(id=category_id).one()
    gameToDelete = session.query(GameItem).filter_by(id=game_id).one()
    if request.method == 'POST':
        session.delete(gameToDelete)
        session.commit()
        flash('Game Item Successfully deleted')
        return redirect(url_for('showGameItems', category_id=category_id))
    else:
        return render_template('deleteGameItem.html', item=gameToDelete)

if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host = '0.0.0.0', port=8000)