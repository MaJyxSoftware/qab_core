import pytest
from qab_core.exception import ConfigNotFoundError, ConfigParseFailureError
from qab_core.config import load_config, CONFIG_DEFAULT

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
