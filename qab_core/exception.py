
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

class ServerCertificateError(Exception):
    '''
    Should be raised when a SSL Certificate error occure when starting
    '''
    pass

class SchedulerInvalidTaskError(Exception):
    '''
    Should be raised when an invalid task is being scheduled
    '''
    pass

class ConsoleRotateError(Exception):
    '''
    Should be raised when an error occure during Console log rotation
    '''
    pass

class ConsoleCompressError(Exception):
    '''
    Should be raised when an error occure during Console log compression
    '''
    pass