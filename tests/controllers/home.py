from qab_core.controller import Controller
from bottle import request

class HomeController(Controller):
    base_route = "/"
    def index(self):
        return f"Hello world!"

    def hello(self, name, lastname=""):
        if lastname:
            lastname = f" {lastname}"
        return f"Hello {name}{lastname}"

    def post(self):
        
        return self.render('This request was a post', dict(request.POST))
