import os

import cherrypy

from app.views import App
from app.settings import Settings

if __name__ == '__main__':
    config = {'server.socket_host': Settings.URL,
              'server.socket_port': Settings.PORT}

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