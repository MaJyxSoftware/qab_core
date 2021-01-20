from qab_core.controller import Controller

class TestController(Controller):
    
    def index(self):
        return "Hello world!"

    def hello(self, firstname, lastname=""):
        return f"Hello {firstname} {lastname}"