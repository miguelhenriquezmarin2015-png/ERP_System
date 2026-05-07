class Usuario:
    def __init__(self,_name,_email,_telefono):
        self.name=_name
        self.email=_email
        self.telefono=_telefono
    def get_name(self):
        return self.name
    def get_email(self):
        return self.email
    def get_telefono(self):
        return self.telefono