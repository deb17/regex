class SSLify:
    def __init__(self, app):
        self.app = app
    def __call__(self, environ, start_response):
        # print('X-Forwarded-Proto is', environ.get('X-Forwarded-Proto'))
        if environ.get('X-Forwarded-Proto') == 'http':
            environ['X-Forwarded-Proto'] = 'https'
        return self.app(environ, start_response)
