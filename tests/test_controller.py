
from qab_core.server import Server
from webtest import TestApp

from tests.controllers.dummy import DummyController

TestApp.__test__ = False

app = Server()
DummyController(app).register()
app.console.is_debug = True
test_app = TestApp(app)

def test_gzip():
    resp = test_app.get('/dummy', status=[200], headers={
        'Accept-Encoding': 'gzip'
    })

    assert resp.status_code == 200
