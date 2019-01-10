import bottle

class SSLify:
    def __init__(self, app):
        self.app = app
    def __call__(self, environ, start_response):
        print('HTTP_X_FORWARDED_PROTO is',
              environ.get('HTTP_X_FORWARDED_PROTO'))
        print(environ)
        if environ.get('HTTP_X_FORWARDED_PROTO') == 'http':
            environ['HTTP_X_FORWARDED_PROTO'] = 'https'
            # newurl = ('https://' + environ.get('HTTP_HOST') +
            #           environ.get('PATH_INFO'))
            # return bottle.redirect(newurl)

        return self.app(environ, start_response)
