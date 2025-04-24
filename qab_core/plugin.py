class Plugin(object):
    api = 2
    name = None
    
    def __init__(self) -> None:
        self.app = None
        
    def setup(self, app) -> None:
        raise NotImplementedError()
    
    def apply(self, callback, route) -> None:
        raise NotImplementedError()
