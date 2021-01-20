import pytest
from webtest import TestApp

from qab_core.server import Server

from tests.controllers.dummy import DummyController

TestApp.__test__ = False

app = Server()
DummyController(app).register()
test_app = TestApp(app)

def test_default():
    resp = test_app.get('/dummy', status=[200])

    assert  b"success" in resp.body

def test_param():
    resp = test_app.get('/dummy/hello/name/John')

    assert resp.body == b"Hello John"

def test_optional_param():
    resp = test_app.get('/dummy/hello/name/John/lastname/Wick')

    assert resp.body == b"Hello John Wick"