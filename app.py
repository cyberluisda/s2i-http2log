#!/usr/bin/python

import json
import logging
from array import array
from logging import DEBUG
from http.server import HTTPServer, BaseHTTPRequestHandler

PORT_NUMBER = 8080
LOG_LEVEL = 'INFO'

_log = logging.getLogger('app')


class HttpServerHandler(BaseHTTPRequestHandler):
    """
    Handler for http request
    """
    # Handle request
    def do_GET(self):
        _log.info("HttpServerHandler:%s %s" % (self.command, self.path))
        self.send_response(200)
        return

    def do_POST(self):
        length = int(self.headers['Content-Length'])
        payload = self.rfile.read(length).decode('UTF-8')
        _log.info("HttpServerHandler:%s %s '%s'" % (self.command, self.path, payload))

        response = json.dumps(
            {
                'result': 'OK'
            }
        )
        self.send_response(200, 'OK')
        self.send_header("Content-Length", len(response))
        self.send_header("Content-Type", "application/json; charset=UTF-8")
        self.end_headers()
        self.wfile.write(response.encode('UTF-8'))

        _log.debug("Response send and flush")
        return

    do_PUT = do_DELETE = do_HEAD = do_POST


def main():
    """
    Entry point of the application
    :return:
    """
    # Initialize logging
    logging.basicConfig(level=LOG_LEVEL)
    try:
        # Create a web server and define the handler to manage the
        # incoming request
        server = HTTPServer(('', PORT_NUMBER), HttpServerHandler)
        _log.info('Starged httpserver on port %s' % PORT_NUMBER)

        # Wait forever for incoming htto requests
        server.serve_forever()

    except KeyboardInterrupt:
        _log.info('^C received, shutting down the web server')
        server.socket.close()


if __name__ == "__main__":
    main()
