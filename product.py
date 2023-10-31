from sqlalchemy import Column, Integer, String, ForeignKey, Table,Float
from config.config import base 





class Product(base):
    
    __tablename__ = "Products"
    
    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    price = Column(Integer)
    
    def as_dict(self):
        return {
            'id': self.id,
            'Name': self.name,
            'Description': self.description,
            'price': self.price
        }



 # Getter para el nombre
    def get_name(self):
        return self._name

    # Setter para el nombre
    def set_name(self, value):
        self._name = value

    # Getter para la descripción
    def get_description(self):
        return self._description

    # Setter para la descripción
    def set_description(self, value):
        self._description = value

    # Getter para el precio
    def get_price(self):
        return self._price

    # Setter para el precio
    def set_price(self, value):
        self._price = value