# -*- coding: utf-8 -*-

from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.web import Application, RequestHandler
from blog import blog

class HTTPHandler(RequestHandler):
    def prepare(self):
        if self.request.protocol == 'http':
            self.redirect('https://' + self.request.host + self.request.uri, permanent = False)

    def get(self):
        self.write("Are you OK")

http_server = Application([
        (r'.*', HTTPHandler),
    ])
http_server.listen(80)

https_server = HTTPServer(WSGIContainer(blog), ssl_options={
    "certfile": "/etc/letsencrypt/live/airtrack.me/fullchain.pem",
    "keyfile": "/etc/letsencrypt/live/airtrack.me/privkey.pem",
    })
https_server.listen(443)
IOLoop.instance().start()
