import pytest
from qab_core.exception import ConfigNotFoundError, ConfigParseFailureError
from qab_core.config import load_config, CONFIG_DEFAULT
import os
import builtins
from unittest import mock

def test_load_default():
    assert load_config() == CONFIG_DEFAULT

def test_load_custom():
    config = load_config('tests/config/custom.json')
    assert config['custom']['foo'] == 'bar'

def test_load_missing():
    with pytest.raises(ConfigNotFoundError):
        load_config('missing.json')

def test_load_bad():
    with pytest.raises(ConfigParseFailureError):
        load_config('tests/config/bad.json')

def test_load_multiple_overrides():
    base = 'tests/config/base.json'
    override = 'tests/config/override.json'
    config = load_config(base, override)
    # 'foo' should be overridden, 'baz' should remain from base
    assert config['custom']['foo'] == 'override'
    assert config['custom']['baz'] == 'qux'

def test_default_config_file_locations():
    # Simulate /etc/qab/app.json, ~/.qab.json, and config.json
    files = {
        '/etc/qab/app.json': '{"server": {"port": 1234}}',
        os.path.expanduser('~/.qab.json'): '{"server": {"address": "127.0.0.1"}}',
        'config.json': '{"server": {"cors_enabled": true}}',
    }
    def fake_exists(path):
        return path in files
    def fake_open(path, *args, **kwargs):
        if path in files:
            return mock.mock_open(read_data=files[path])()
        raise FileNotFoundError(path)
    with mock.patch('os.path.exists', fake_exists), \
         mock.patch('builtins.open', fake_open):
        config = load_config('/etc/qab/app.json', os.path.expanduser('~/.qab.json'), 'config.json')
        assert config['server']['port'] == 1234
        assert config['server']['address'] == '127.0.0.1'
        assert config['server']['cors_enabled'] is True
