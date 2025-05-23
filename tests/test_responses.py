import os
import subprocess
from multiprocessing import Process
import time

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

DUMMY_EP = "/dummy"

@pytest.fixture(autouse=True, scope="session")
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

def test_gzip():
    resp = test_app.get(DUMMY_EP, status=[200], headers={
        'Accept-Encoding': 'gzip'
    })

    assert resp.status_code == 200

def test_cors():
    ajax_headers = {
        'X-Requested-With': 'XMLHttpRequest',
        'Origin': 'http://localhost:80'
    }

    # Test CORS disabled
    app.config['server']['cors_enabled'] = False
    resp = test_app.get(DUMMY_EP, status=[200], headers=ajax_headers)
    assert resp.headers.get('Access-Control-Allow-Origin') == None

    # Test CORS enabled
    app.config['server']['cors_enabled'] = True
    resp = test_app.get(DUMMY_EP, status=[200], headers=ajax_headers)
    assert resp.headers.get('Access-Control-Allow-Origin')

    # Test CORS enabled + good host
    app.config['server']['cors_domains'] = [ 'localhost:80' ]
    resp = test_app.get(DUMMY_EP, status=[200], headers=ajax_headers)
    assert resp.headers.get('Access-Control-Allow-Origin')

    # Test CORS enbled + bad host
    app.config['server']['cors_domains'] = [ 'wronghost.ltd' ]
    resp = test_app.get(DUMMY_EP, status=[200], headers=ajax_headers)
    assert resp.headers.get('Access-Control-Allow-Origin') == None

def test_cert():
    certs_path='certs/'
    expired_certs="tests/expired_certs"
    if os.path.exists(certs_path):
        for file in os.scandir(certs_path):
            os.remove(file.path)

    # No certs + No gen
    app.config['server']['generate_ssl'] = False
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

def test_method_option():
    resp = test_app.options(DUMMY_EP, status=[200])

    assert resp.body == b"OK"

def test_redirect_home():
    resp = test_app.get('/', status=[302])

    assert resp.headers['location']
