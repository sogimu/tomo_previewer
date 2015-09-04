import os

import cherrypy

from app.views import App

if __name__ == '__main__':
    config = {'server.socket_host': '127.0.0.1',
              'server.socket_port': 8080}

    cherrypy.config.update(config)

    conf = {
        '/static': {
        'tools.staticdir.on': True,
        'tools.staticdir.dir': os.path.join(os.getcwd(), 'app/static')
        },
        '/': {
        'tools.staticdir.on': True,
        'tools.staticdir.dir': os.path.join(os.getcwd(), 'data')
        }

    }

    root = App()

    cherrypy.quickstart( root, '/', conf)