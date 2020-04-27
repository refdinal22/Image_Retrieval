# 1 - imports
import json
from sqlalchemy import func
from . import base
from .model import Product
from sqlalchemy.ext.declarative import DeclarativeMeta

class DAO:
	def __init__(self):
		self.session = base.Session()

	def getAll(self):
		products = self.session.query(Product).all()		
		return products		

	def getProduct(self, ids):
		q = self.session.query(Product)
		products = q.filter(Product.id.in_(ids)).order_by(func.field(Product.id, *ids))
		return products

	def insert(self, name, price, image):
		product = Product(name, price, image)
		self.session.add(product)

		self.session.commit()
		self.session.close()

# if __name__ == '__main__':
	# database = Database()

# 	# Get Product by Id
# 	id = [2,1,3,4]
# 	products = database.getProduct(id)
# 	print('\n### All Products Order By ID:')
# 	for product in products:
# 		print(f'{product.id} . {product.name} price {product.price}')    
# 	print('')

# 	# Insert
# 	database.insert("Short pant", 300000)
# 	database.insert("Pant", 100000)

# 	# Get All Product
# 	products = database.getAll()
# 	print('\n### All Products:')
# 	for product in products:
# 		print(f'{product.id} . {product.name} price {product.price}')    
# 	print('')

        

