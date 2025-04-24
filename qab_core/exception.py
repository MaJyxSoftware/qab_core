
class ConfigNotFoundError(Exception):
    def __init__(self, file_path, message="Configuration file not found"):
        self.file_path = file_path
        self.message = f"{message}: {file_path}"
        super().__init__(self.message)

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