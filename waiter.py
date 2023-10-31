from sqlalchemy import Column, Integer, String
from config.config import base 



class Waiter(base):
    __tablename__ ="Waiters"
    
    id = Column(Integer, primary_key=True)
    username = Column(String)
    password= Column(String)
    
    def as_dict(self):
        return {
            'id': self.id,
            'Username': self.username
        }
    
    
 # Getter para el nombre de usuario
    def get_username(self):
        return self._username

    # Setter para el nombre de usuario
    def set_username(self, value):
        self._username = value

    # Getter para la contraseña
    def get_password(self):
        return self._password

    # Setter para la contraseña
    def set_password(self, value):
        self._password = value
