
from qab_core.server import Server
from webtest import TestApp

from tests.controllers.dummy import DummyController
from tests.controllers.home import HomeController

TestApp.__test__ = False

app = Server()
DummyController(app).register()
HomeController(app).register()
app.console.is_debug = True
test_app = TestApp(app)

def test_default():
    resp = test_app.get('/dummy', status=[200])

    assert  b"success" in resp.body

def test_param():
    resp = test_app.get('/dummy/hello/name/John', status=[200])

    assert resp.body == b"Hello John"

def test_optional_param():
    resp = test_app.get('/dummy/hello/name/John/lastname/Wick', status=[200])

    assert resp.body == b"Hello John Wick"

def test_post():
    resp = test_app.post('/dummy/post', {
        'foo': 'bar'
    }, status=[200])

    assert resp.json['data']['foo'] == "bar"

def test_rebased_route():
    resp = test_app.get('/', status=[200])

    assert resp.body == b"Hello world!"
