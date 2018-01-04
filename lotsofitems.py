from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
 
from database_setup import User, Category, Item

engine = create_engine('sqlite:///categoryitems.db')

Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)

session = DBSession()

#add user1
default_user = user(id=1, name="User1", email="default@email.com")
session.add(default_user)

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
item1 = item(name="", id=1, description="This is the best action game of the year watch out Witch Hunter", price="$49.99", category_id=1, user_id=1)


print "added items to catalog"