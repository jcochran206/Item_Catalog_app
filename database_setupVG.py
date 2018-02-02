from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
 
Base = declarative_base()

class GameCategory(Base):
    __tablename__ = 'category'
   
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)

    @property
    def serialize(self):
       """Return object data in easily serializeable format"""
       return {
           'name'         : self.name,
           'id'           : self.id,
       }
 
class GameItem(Base):
    __tablename__ = 'game_item'


    name =Column(String(80), nullable = False)
    id = Column(Integer, primary_key = True)
    description = Column(String(250))
    price = Column(String(8))
    image = Column(String(250))
    systemType = Column(String(8))
    category_id = Column(Integer,ForeignKey('category.id')) #foregin key item from outer table
    category = relationship(GameCategory) #table use to relate items


    @property
    def serialize(self):
       """Return object data in easily serializeable format"""
       return {
           'name'         : self.name,
           'description'         : self.description,
           'id'         : self.id,
           'price'         : self.price,
           'image'      : self.image,
           'systemType'         : self.systemType,
       }



engine = create_engine('sqlite:///videogames.db')
 

Base.metadata.create_all(engine)