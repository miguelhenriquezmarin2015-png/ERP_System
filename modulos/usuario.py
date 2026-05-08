from abc import ABC, abstractmethod
from especialidades import enums
class Persona(ABC):
    @abstractmethod
    def __init__(self,_name,_cedula,_telefono):
        self.name=_name
        self.cedula=_cedula
        self.telefono=_telefono
    def get_name(self):
        return self.name
    def get_cedula(self):
        return self.cedula 
    def get_telefono(self):
        return self.telefono
    
class Cliente(Persona):
    def __init__(self,_name,_cedula,_telefono,_tipo:Persona):
        super().__init__(_name,_cedula,_telefono)
        self.tipo=_tipo