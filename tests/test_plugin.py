import pytest

from qab_core.server import Server
from qab_core.plugin import Plugin

class BadPlugin(Plugin):
    pass

class Bad2Plugin(Plugin):
    
    def setup(self, app):
        print("Plugin setup in defined")

def test_bad():
    app = Server()
    bad = BadPlugin()
    bad2 = Bad2Plugin()
    
    with pytest.raises(NotImplementedError):
        bad.setup(app)
        
    with pytest.raises(NotImplementedError):
        bad.apply(None, None)

    bad2.setup(app)
    
    with pytest.raises(NotImplementedError):
        bad.apply(None, None)
