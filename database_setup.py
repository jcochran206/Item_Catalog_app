import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy import create_engine, event
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
	__tablename__ = 'user'

	id = Column(Integer, primary_key=True)
	name = Column(String(250), nullable=False)
	email = Column(String(250), nullable=False)

class Category(Base):
	__tablename__ = 'category'

	id = Column(Integer, primary_key=True)
	name = Column(String(250), nullable=False)

	@property 
	def serialize(self):
		return{
			'name' : self.name,
			'id' : self.id
		}

class Item(Base):
	__tablename__ = 'item'

	name = Column(String(100), nullable=False)
	id = Column(Integer, primary_key=True)
	description = Column(String(250))
	price = Column(String(10))
	category_id = Column(Integer, ForeignKey('category.id'))
	category = relationship(Category)
	user_id = Column(Integer, ForeignKey('user.id'))
	user = relationship(User)

	@property
	def serialize(self):
		return {
		'name' : self.name,
		'description' : self.description,
		'id' : self.id,
		'price' : self.price,
		'category' : self.category_id 
		}

engine = create_engine('sqlite:///categoryitems.db')

Base.metadata.create_all(engine)
		