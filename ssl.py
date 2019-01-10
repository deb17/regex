import bottle

class SSLify:
    def __init__(self, app):
        self.app = app
    def __call__(self, environ, start_response):
        print('X-Forwarded-Proto is', environ.get('X-Forwarded-Proto'))
        print(environ)
        if environ.get('X-Forwarded-Proto') == 'http':
            pass
            # return bottle.redirect(newurl)
        return self.app(environ, start_response)
