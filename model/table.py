from sqlalchemy import Column, Integer, String
from config.config import base

class Table(base):
    __tablename__ = "Tables"
    
    id = Column(Integer, primary_key=True)
    number = Column(Integer)
    capacity = Column(Integer)
    state = Column(String)
    
    
    def as_dict(self):
        return {
            'id': self.id,
            'Number': self.number,
            'Capacity': self.capacity,
            'State': self.state
        }
    

 # Getter para el número de mesa
    def get_number(self):
        return self._number

    # Setter para el número de mesa
    def set_number(self, value):
        self._number = value

    # Getter para la capacidad
    def get_capacity(self):
        return self._capacity

    # Setter para la capacidad
    def set_capacity(self, value):
        self._capacity = value

    # Getter para el estado
    def get_state(self):
        return self._state

    # Setter para el estado
    def set_state(self, value):
        self._state = value

        