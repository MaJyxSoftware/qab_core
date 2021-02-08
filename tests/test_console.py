import os
import datetime

import pytest

from qab_core.server import Server
from qab_core.exception import ConsoleCompressError, ConsoleRotateError

app = Server()
app.console.is_debug = True

def test_log():
    app.console.log('Test log')
    
    with open(app.console.console_log, 'r') as cf:
        lines = cf.readlines()
        assert lines[-1].rstrip().endswith('Test log')

def test_rotate():
    yesterday = datetime.date.today() - datetime.timedelta(days=1)
    yesterdays_date = yesterday.strftime('%Y%m%d')
    dest = f"{app.console.console_log}.{yesterdays_date}"

    if os.path.exists(dest):
        os.remove(dest)

    app.console.rotate(app.console.console_log)
    assert os.path.exists(dest)

    with pytest.raises(ConsoleRotateError):
        app.console.rotate(app.console.console_log)

def test_compress():
    yesterday = datetime.date.today() - datetime.timedelta(days=1)
    yesterdays_date = yesterday.strftime('%Y%m%d')
    src = f"{app.console.console_log}.{yesterdays_date}"
    dest = f"{app.console.console_log}.{yesterdays_date}.tar.gz"

    if os.path.exists(dest):
        os.remove(dest)

    if not os.path.exists(src):
        app.console.rotate(app.console.console_log)
    app.console.compress()
    assert os.path.exists(dest)

    app.console.rotate(app.console.console_log)
    with pytest.raises(ConsoleCompressError):
        app.console.compress()

    if os.path.exists(src):
        # Remove rotated files that couldn't be compressed
        os.remove(src)