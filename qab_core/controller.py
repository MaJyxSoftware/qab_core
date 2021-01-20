#!/usr/bin/env python
import gzip
import json

from bottle import request, response

class Controller(object):

    pass_method = [
        "__init__"
    ]

    def __init__(self, app):
        self.app = app
        self.content_type = 'text/html'
    
    def __str__(self):
        return self.__class__.__name__

    def register(self):
        '''
        Register current controler
        '''
        self.app.register(self)

    def render(self, msg, data=None, status="success", code=200):
        '''
        Render response
        '''
        if isinstance(data, str):
            response.content_type = self.content_type
        else:
            response.content_type = 'application/json'

        response.status = code
        res = {
            "status": status,
            "message": msg,
            "code": code
        }

        if data is not None:
            res["data"] = data

        res = json.dumps(res)

        if 'gzip' in request.get_header('accept-encoding', ""):
            response.set_header("Content-Encoding", "gzip")
            res = gzip.compress(res.encode('utf-8'), compresslevel=5)
            self.app.console.debug("GZip response (req header: {})".format(request.get_header('accept-encoding', "")))

        response.add_header("X-Response-Size", len(res))

        self.app.console.debug("Data sent: {} (size: {})".format(data, len(res)))

        return res

    def abort(self, code=404, text="Not found"):
        '''
        Send error response
        '''

        return self.render("Error {}: {}".format(code, text), text, "error", code)
