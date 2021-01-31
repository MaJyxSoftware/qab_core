import os
import tarfile
import socket
import datetime

from qab_core.exception import ConsoleCompressError, ConsoleRotateError

def compress(tar_file, files):
    """
    Adds files (`members`) to a tar_file and compress it
    """
    # open file for gzip compressed writing
    if os.path.exists(dest):
        raise ConsoleCompressError(f"Couldn't compress the log, archive {tar_file} already exists")

    tar = tarfile.open(tar_file, mode="w:gz")
    for f in files:
        # add file/folder/link to the tar file (compress)
        tar.add(f)
    # close the file
    tar.close()

class Console(object):

    def __init__(self, quiet=False, nolog=False, debug=False, log_dir="logs/"):
        self.quiet = quiet
        self.nolog = nolog
        self.is_debug = debug
        self.hostname = socket.gethostname()
        self.log_dir = log_dir

        self.console_log = os.path.join(self.log_dir, "console.log")
        self.error_log = os.path.join(self.log_dir, "error.log")

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

            if self.need_rotation(self.console_log):
                self.rotate(self.console_log)

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
            if self.need_rotation(self.error_log):
                self.rotate(self.error_log)

            with open(self.error_log, "a") as log_file:
                log_file.write("[{}/{}][ERROR] {}\n".format(self.hostname, now, text))

    def need_rotation(self, log_file):
        '''
        Check if log file need rotation
        '''

        if os.path.exists(log_file):
            last_modified = datetime.datetime.fromtimestamp(os.path.getmtime(log_file))
            today =  datetime.date.today()
            start = datetime.datetime(today.year, today.month, today.day)

            if last_modified < start:
                self.debug(f"Log file {log_file} need rotation")
                return True

        return False

    def rotate(self, log_file):
        '''
        Rotate log file
        '''

        self.debug(f"Rotating log file {log_file}")
        yesterday = datetime.date.today() - datetime.timedelta(days=1)
        yesterdays_date = yesterday.strftime('%Y%m%d')
        if os.path.exists(log_file):
            dest = f"{log_file}.{yesterdays_date}"
            if os.path.exists(dest):
                raise ConsoleRotateError(f"Couldn't rotate log file, file {dest} already exists")
            self.debug(f"Rotating log file {log_file} to {dest}")
            os.rename(log_file, dest)


    def compress(self):
        '''
        Compress rotated log files
        '''
        self.debug(f"Compressing rotated log files")

        for log_file in os.listdir(self.log_dir):
            if not log_file.endswith('.log') and not log_file.endswith('.tar.gz'):
                src = os.path.join(self.log_dir, log_file)
                dest = os.path.join(self.log_dir, f"{log_file}.tar.gz")
                self.debug(f"Compressing log file {src} to {dest}")
                compress(dest, [src])
                os.remove(src)
