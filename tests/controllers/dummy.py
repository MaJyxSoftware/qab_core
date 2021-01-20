from qab_core.controller import Controller

class DummyController(Controller):
    
    def index(self):
        return self.render("Mon message", data=self.app.config)

    def hello(self, name, lastname=""):
        if lastname:
            lastname = f" {lastname}"
        return f"Hello {name}{lastname}"