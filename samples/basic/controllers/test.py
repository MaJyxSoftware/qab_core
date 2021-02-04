from qab_core.controller import Controller
from decorator import decorator

@decorator
def test_decorator(func, *args, **kwargs):
    return func(*args, **kwargs)

class TestController(Controller):
    
    @test_decorator
    def index(self):
        return "Hello world!"

    def hello(self, firstname, lastname=""):
        return f"Hello {firstname} {lastname}"