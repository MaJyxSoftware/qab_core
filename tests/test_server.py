import os
import time

from qab_core.server import Server, _gen_cryptography
from qab_core.exception import ServerCertificateError

def test_server_start_full_coverage():
    import shutil
    from unittest.mock import patch
    from qab_core.server import Server

    app = Server()  # Re-instantiate to ensure clean state

    cert_path = app.config['server']['certificate']
    key_path = app.config['server']['private_key']
    certs_dir = os.path.dirname(cert_path)

    # Clean up certs
    if os.path.exists(certs_dir):
        for file in os.scandir(certs_dir):
            os.remove(file.path)
    else:
        os.makedirs(certs_dir)

    # --- Error path: SSL generation disabled, missing certs ---
    app.config['server']['generate_ssl'] = False
    with patch.object(app, 'run') as mock_run, \
         patch.object(app.scheduler, 'start') as mock_sched_start, \
         patch.object(app.scheduler, 'stop') as mock_sched_stop:
        mock_run.side_effect = Exception('Should not be called')
        with patch.object(app.console, 'error') as mock_log_err:
            try:
                app.start()
                assert False, 'Expected ServerCertificateError'
            except ServerCertificateError:
                pass
            mock_log_err.assert_any_call('Invalid cetificates, please check error above!')
        mock_sched_start.assert_not_called()
        mock_run.assert_not_called()

    # --- Success path: SSL generation enabled, missing certs ---
    app.config['server']['generate_ssl'] = True
    with patch.object(app, 'run') as mock_run, \
         patch.object(app.scheduler, 'start') as mock_sched_start, \
         patch.object(app.scheduler, 'stop') as mock_sched_stop:
        mock_run.return_value = None
        mock_sched_start.return_value = None
        mock_sched_stop.return_value = None
        app.start()
        assert os.path.exists(cert_path)
        assert os.path.exists(key_path)
        mock_sched_start.assert_called()
        mock_run.assert_called()
        mock_sched_stop.assert_not_called()

    # Clean up certs after test
    if os.path.exists(cert_path):
        os.remove(cert_path)
    if os.path.exists(key_path):
        os.remove(key_path)
