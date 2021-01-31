import time
from datetime import datetime
import os
import random

import pytest

from qab_core.server import Server
from qab_core.exception import SchedulerInvalidTaskError

from tests.controllers.dummy import DummyController

app = Server()
DummyController(app).register()
app.console.is_debug = True

DEFAULT_TMP_FILE="/tmp/default_scheduler.tmp"

def touch_tmp_with_arg(filename):
    touch_tmp(filename=filename)

def touch_tmp(filename=DEFAULT_TMP_FILE):
    app.console.debug(f"In scheduled method with filename {filename}")
    open(filename, "w").close()

def test_scheduler():
    '''
    test default scheduler behavior
    '''

    if os.path.exists(DEFAULT_TMP_FILE):
        os.remove(DEFAULT_TMP_FILE)

    arg_file = "/tmp/arg_scheduler.tmp"
    if os.path.exists(arg_file):
        os.remove(arg_file)

    kwarg_file = "/tmp/kwarg_scheduler.tmp"
    if os.path.exists(kwarg_file):
        os.remove(kwarg_file)

    recurence = "* * * * *"
    app.scheduler.add(recurence, touch_tmp)
    app.scheduler.add(recurence, touch_tmp_with_arg, arg_file)
    app.scheduler.add(recurence, touch_tmp, filename=kwarg_file)
    with pytest.raises(SchedulerInvalidTaskError):
        app.scheduler.add("* * * * a", touch_tmp)

    app.scheduler.start()
    time.sleep(60 - datetime.now().second + 5)

    app.scheduler.stop()

    assert os.path.exists(DEFAULT_TMP_FILE)
    assert os.path.exists(arg_file)
    assert os.path.exists(kwarg_file)
