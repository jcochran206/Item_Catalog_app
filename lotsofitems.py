from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
 
from database_setup import Base, User, Category, Item

engine = create_engine('sqlite:///categoryitems.db')

Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)

session = DBSession()

#add user1
#default_user = user(id=1, name="User1", email="default@email.com")
#session.add(default_user)

#add categories
category1 = Category(id=1, name="Action")
session.add(category1)
session.commit()

category2 = Category(id=2, name="Sports")
session.add(category2)
session.commit()

category3 = Category(id=3, name="RPG")
session.add(category3)
session.commit()

category4 = Category(id=4, name="Shooter")
session.add(category4)
session.commit()

category5 = Category(id=5, name="Strategy")
session.add(category5)
session.commit()

#add items
item1 = item(name="Naruto Shadows of Leaf", id=1, description="This is the best action game of the year watch out Witch Hunter", price="$49.99", category_id=1, user_id=1)
session.add(item1)
session.commit()

item2 = item(name="Hero Marksman", id=2, description="This is better then star wars battlefront", price="$39.99", category_id=1, user_id=1)
session.add(item2)
session.commit()

item3 = item(name="FIFA 2018", id=3, description="Best Soccer game ever El Tornado", price="$29.99", category_id=2, user_id=1)
session.add(item3)
session.commit()

item4 = item(name="Madden 2018", id=4, description="Is there any other football game", price="$49.99", category_id=2, user_id=1)
session.add(item4)
session.commit()

item5 = item(name="Final Fantasy VII", id=5, description="McCloud sword-style art", price="$49.99", category_id=3, user_id=1)
session.add(item5)
session.commit()

item6 = item(name="Call of Duty WWII", id=6, description="Call of Duty WWII is the best since first COD", price="$89.99", category_id=4, user_id=1)
session.add(item6)
session.commit()

item7 = item(name="Destiny 2", id=7, description="This franchise gives halo a run for its money", price="$49.99", category_id=4, user_id=1)
session.add(item7)
session.commit()

item8 = item(name="Chess", id=8, description="This is a classic Strategy game for the ages", price="$19.99", category_id=5, user_id=1)
session.add(item8)
session.commit()


#add 

print "added items to catalog"