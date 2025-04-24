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
        
        if response.content_type == 'application/json':
            res = {
                "status": status,
                "message": msg,
                "code": code
            }

            if data is not None:
                res["data"] = data

            res = json.dumps(res)
        else:
            res = data
            
            if msg:
                response.add_header('X-Server-Msg', msg)

        self.app.console.debug("Data sent: {} (size: {})".format(data, len(res)))

        return res

    def abort(self, code=404, text="Not found"):
        '''
        Send error response
        '''

        return self.render("Error {}: {}".format(code, text), {'error': text}, "error", code)
