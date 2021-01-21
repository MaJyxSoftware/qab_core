import os
import subprocess

import pytest
from webtest import TestApp
import OpenSSL

from qab_core.server import Server, _gen_cryptography
from qab_core.exception import ServerCertificateError

from tests.controllers.dummy import DummyController

TestApp.__test__ = False

app = Server()
DummyController(app).register()
app.console.is_debug = True
test_app = TestApp(app)

@pytest.fixture(scope="session")
def start_server():
    my_env = os.environ.copy()
    my_env["GENERATE_SSL"] = "true"
    srv = subprocess.Popen(
        [
            "python",
            "sample/basic/start.py"
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        env=my_env
    )

    assert not srv.poll(), srv.stdout.read().decode("utf-8")

    yield srv
    # Shut it down at the end of the pytest session
    srv.terminate()

def test_default():
    resp = test_app.get('/dummy', status=[200])

    assert  b"success" in resp.body

def test_param():
    resp = test_app.get('/dummy/hello/name/John', status=[200])

    assert resp.body == b"Hello John"

def test_optional_param():
    resp = test_app.get('/dummy/hello/name/John/lastname/Wick', status=[200])

    assert resp.body == b"Hello John Wick"

def test_cors():
    resp = test_app.get('/dummy', status=[200])
    assert resp.headers.get('Access-Control-Allow-Origin') == None

    # Test CORS enabled
    app.config['server']['cors_enabled'] = True
    resp = test_app.get('/dummy', status=[200])
    assert resp.headers.get('Access-Control-Allow-Origin')

    # Test CORS enabled + good host
    app.config['server']['cors_domains'] = [ 'localhost:80' ]
    resp = test_app.get('/dummy', status=[200])
    assert resp.headers.get('Access-Control-Allow-Origin')

    # Test CORS enbled + bad host
    app.config['server']['cors_domains'] = [ 'wronghost.ltd' ]
    resp = test_app.get('/dummy', status=[200])
    assert resp.headers.get('Access-Control-Allow-Origin') == None

def test_cert():
    certs_path='certs/'
    expired_certs="tests/expired_certs"
    if os.path.exists(certs_path):
        for file in os.scandir(certs_path):
            os.remove(file.path)

    # No certs + No gen
    assert app.check_certificate() == False

    # No cert + self-signed gen
    app.config['server']['generate_ssl'] = True
    assert app.check_certificate() == True

    # Expired cert + no gen
    app.config['server']['generate_ssl'] = False
    if os.path.exists(expired_certs):
        for file in os.scandir(expired_certs):
            dest_name = file.name.replace('.test', '')
            print(f"Copy {file.path} to {os.path.join(certs_path, dest_name)}")
            with open(file.path, 'rb') as src_file, open(os.path.join(certs_path, dest_name), 'wb') as dst_file:
                dst_file.write(src_file.read())
    assert app.check_certificate() == False

    # Expired cert + self-signed gen
    app.config['server']['generate_ssl'] = True
    assert app.check_certificate() == True

    # Certs OK
    assert app.check_certificate() == True

def test_alternative_cert_gen():
    pub, _ = _gen_cryptography()

    x509 = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, pub)

    assert x509.digest('sha1')

def test_start(start_server):
    # Disable self signed cert generation
    certs_path='certs/'
    if os.path.exists(certs_path):
        for file in os.scandir(certs_path):
            os.remove(file.path)

    app.config['server']['generate_ssl'] = False

    with pytest.raises(ServerCertificateError):
        app.start()
