from qab_core.server import Server

from controllers.test import TestController


def start():
    app = Server()
    
    TestController(app).register()

    app.start()

if __name__ == "__main__":
    start()