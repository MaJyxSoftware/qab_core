
class ConfigNotFoundError(Exception):
    '''
    Should be raised when trying tp load a configuration file that doesn't exists
    '''
    pass

class ConfigParseFailureError(Exception):
    '''
    Should be raised when the configuration file couldn't be parsed (syntax error)
    '''
    pass
