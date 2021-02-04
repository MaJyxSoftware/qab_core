from qab_core.controller import Controller
from bottle import request

from decorator import decorator

@decorator
def test_decorator(func, *args, **kwargs):
    return func(*args, **kwargs)

class DummyController(Controller):
    
    def index(self):
        return self.render("Mon message", data=self.app.config)

    def hello(self, name, lastname=""):
        if lastname:
            lastname = f" {lastname}"
        return f"Hello {name}{lastname}"

    def post(self):
        
        return self.render('This request was a post', dict(request.POST))

    def multi(self, word1="", word2=""):
        return f"Say {word1} {word2}"

    @test_decorator
    def deco(self):
        return "decorated"