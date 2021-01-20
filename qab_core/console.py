import os
import socket
import datetime

class Console(object):

    def __init__(self, quiet=False, nolog=False, debug=False, log_dir="logs/"):
        self.quiet = quiet
        self.nolog = nolog
        self.is_debug = debug
        self.hostname = socket.gethostname()
        self.log_dir = log_dir

        self.console_log = "{}console.log".format(self.log_dir)
        self.access_log = "{}access.log".format(self.log_dir)
        self.error_log = "{}error.log".format(self.log_dir)
    
    def access(self, msg):
        '''
        Write access log with apache like log format
        '''
        if not os.path.exists(self.log_dir):
                os.makedirs(self.log_dir)

        with open(self.access_log, "a") as log_file:
            log_file.write("{}\n".format(msg))

    def log(self, text, log_type="INFO"):
        '''
        Write log message
        '''
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
        if not self.quiet:
            print("[{}/{}][{}] {}".format(self.hostname, now, log_type, text))

        if not self.nolog:
            if not os.path.exists(self.log_dir):
                os.makedirs(self.log_dir)

            with open(self.console_log, "a") as log_file:
                log_file.write("[{}/{}][{}] {}\n".format(self.hostname, now, log_type, text))

    def debug(self, text):
        '''
        Write debug message
        '''
        if self.is_debug:
            self.log(text, log_type="DEBUG")

    def error(self, text):
        '''
        Write error message
        '''
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
        if not self.quiet:
            self.log(text, log_type="ERROR")

        if not self.nolog:
            with open(self.error_log, "a") as log_file:
                log_file.write("[{}/{}][ERROR] {}\n".format(self.hostname, now, text))

    def clean_log(self):
        '''
        Truncate error & debug log files
        '''
        open(self.console_log, "w")
        open(self.error_log, "w")
