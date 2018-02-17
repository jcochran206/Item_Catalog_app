from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setupVG import GameCategory, Base, GameItem

engine = create_engine('sqlite:///videogames.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()

#first category of games
category1 = GameCategory(name="Sports")

session.add(category1)
session.commit()

gameItem1 = GameItem(name="Madden 2018", description="Go Hawks",
                     price="$35.50", image="/static/images/gameitem1.jpg", systemType="PS4", category=category1)

session.add(gameItem1)
session.commit() 

gameItem2 = GameItem(name="Tecmo bowl classic", description="8bit classic mania",
                     price="$25.50", image="/static/images/gameitem2.jpg", systemType="PS4", category=category1)

session.add(gameItem2)
session.commit()


gameItem3 = GameItem(name="FIFA 2018", description="Ronaldo El Tornado",
                     price="$20.99", image="/static/images/gameitem3.jpg", systemType="xbox", category=category1)

session.add(gameItem3)
session.commit()

#secondary category of games
category2 = GameCategory(name="Action")

session.add(category2)
session.commit()

gameItem4 = GameItem(name="UFC3", description="Connor the Hammer",
                     price="$45.50", image="/static/images/gameitem4.jpg", systemType="PS4", category=category2)

session.add(gameItem4)
session.commit() 

gameItem5 = GameItem(name="Call of Duty WW2", description="Saving Private Cochran",
                     price="$55.50", image="/static/images/gameitem5.jpg", systemType="PS4", category=category2)

session.add(gameItem5)
session.commit()

#Category 3 
category3 = GameCategory(name="RPG")

session.add(category3)
session.commit()

gameItem6 = GameItem(name="MonsterHunter", description="Whole alot of flying dragon prepare of war",
                     price="$45.50", image="/static/images/gameitem6.jpg", systemType="PS4", category=category3)

session.add(gameItem6)
session.commit()

gameItem7 = GameItem(name="Destiny 2", description="where is my glimmer boys",
                     price="$45.50", image="/static/images/gameitem7.jpg", systemType="xbox", category=category3)

session.add(gameItem7)
session.commit()

gameItem8 = GameItem(name="Cars 3", description="fabulous lightning mcqueen",
                     price="$45.50", image="/static/images/gameitem8.jpg", systemType="switch", category=category1)

session.add(gameItem8)
session.commit()

gameItem9 = GameItem(name="Has Been Heros", description="Here we come to save the day",
                     price="$25.50", image="/static/images/gameitem9.jpg", systemType="switch", category=category2)

session.add(gameItem9)
session.commit()


print "added videogames items!"