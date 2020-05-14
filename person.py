class Person:
    def __init__(self, addr, client):
        self.name = None
        self.addr = addr
        self.client = client
    def set_name(self, name):
        self.name = name
    def __repr__(self):
        return f'Person({self.name}, {self.addr}'