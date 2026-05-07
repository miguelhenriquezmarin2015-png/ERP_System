class Inventario:
    def __init__(self,_id,_nombre,_cantidad,_precio):
        self.id=_id
        self.nombre=_nombre
        self.cantidad=_cantidad
        self.precio=_precio
    def get_id(self):
        return self.id
    def get_nombre(self):
        return self.nombre
    def get_cantidad(self):
        return self.cantidad
    def get_precio(self):
        return self.precio
    def get_precio(self,id):
        if self.id == id:
            return self.precio
        else:
            return None
    