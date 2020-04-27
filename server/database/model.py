from sqlalchemy import Column, String, Integer

from . import base
from sqlalchemy_serializer import SerializerMixin

class Product(base.Base, SerializerMixin):
	__tablename__ = 'product'

	id = Column(Integer, primary_key=True)
	name = Column(String)
	price = Column(Integer)
	image = Column(String)

	def __init__(self, name, price, image):
		self.name = name
		self.price = price
		self.image = image
