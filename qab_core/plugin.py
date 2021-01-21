import gzip

from bottle import request, response

class GzipPlugin(object):
    name = "gzip_plugin"
    api = 2

    def __init__(self):
        self.app = None

    def setup(self, app):
        """Handle plugin install"""
        self.app = app

    def apply(self, callback, route):
        """Handle route callbacks"""
        def wrapper(*args, **kwargs):
            """Apply GZip to the body and add appriopriate header"""
            body = callback(*args, **kwargs)
            

            if 'gzip' in request.get_header('accept-encoding', ""):
                response.set_header("Content-Encoding", "gzip")
                body = gzip.compress(body.encode('utf-8'), compresslevel=5)
                self.app.console.debug("GZip response (req header: {})".format(request.get_header('accept-encoding', "")))
            return body

        return wrapper