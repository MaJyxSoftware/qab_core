
from qab_core.server import Server
from webtest import TestApp

from tests.controllers.dummy import DummyController

TestApp.__test__ = False

app = Server()
DummyController(app).register()
app.console.is_debug = True
test_app = TestApp(app)

def test_post():
    resp = test_app.post('/dummy/post', {
        'foo': 'bar'
    }, status=[200])

    assert resp.json['data']['foo'] == "bar"


