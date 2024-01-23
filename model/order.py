from sqlalchemy import Column, Integer, String, ForeignKey, Table,Float,DateTime
from config.config import base
from sqlalchemy.orm import relationship, Mapped
from.product import Product
from typing import List

class Order(base):
    __tablename__ ="Orders"
    
    id = Column(Integer, primary_key=True)
    order_number = Column(Integer)
    total = Column(Float)
    state = Column(String)
    assigned_table = Column(Integer, ForeignKey('Tables.number'))
    products: Mapped[List[Product]]  = relationship("Product", secondary="order_product")
    assigned_waiter = Column(Integer, ForeignKey('Waiters.id'))
    hour = Column(DateTime)
    
    order_product = Table('order_product', base.metadata,Column('order_id',Integer, ForeignKey('Orders.id')),
                          Column('Product_id',Integer, ForeignKey('Products.id')))
    
    
    def as_dict(self):
        return {
            'order_number': self.order_number,
            'total': self.total,
            'state': self.state,
            'assigned_Table': self.assigned_table,
            'products': self.products,
            'assigned_Waiter': self.assigned_waiter
        }
        
        
    def calculate_total(self):
        total = 0.0
        for Product in self.products:
            total += Product.price
        return total
        
    
    
 # Getter para el número de pedido
    def get_order_number(self):
        return self._order_number

    # Setter para el número de pedido
    def set_order_number(self, value):
        self._order_number = value

    # Getter para la lista de productos
    def get_products(self):
        return self._products

    # Setter para la lista de productos
    def set_products(self, value):
        self._products = value

    # Getter para el total
    def get_total(self):
        return self._total

    # Setter para el total
    def set_total(self, value):
        self._total = value

    # Getter para el estado
    def get_state(self):
        return self._state

    # Setter para el estado
    def set_state(self, value):
        self._state = value

    # Getter para la mesa asignada
    def get_assigned_table(self):
        return self._assigned_table

    # Setter para la mesa asignada
    def set_assigned_table(self, value):
        self._assigned_table = value
    # Getter para el número de pedido
    def get_assigned_waiter(self):
        return self._assigned_waiter

    # Setter para el número de pedido
    def set_assigned_waiter(self, value):
        self._assigned_waiter = value



    