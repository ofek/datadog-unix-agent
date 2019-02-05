# Unless explicitly stated otherwise all files in this repository are licensed
# under the Apache License Version 2.0.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2018 Datadog, Inc.

import logging

import tornado.httpserver
import tornado.ioloop
import tornado.web

from .handlers import APIStatusHandler


log = logging.getLogger(__name__)


class APIServer(object):

    def __init__(self, port, aggregator_stats):
        # start API
        self._port = port
        self._app = tornado.web.Application([
            (r"/status", APIStatusHandler, dict(aggregator_stats=aggregator_stats)),
        ])
        self._server = tornado.httpserver.HTTPServer(self._app)
        self._ioloop = tornado.ioloop.IOLoop.current()

    def stop(self):
        self._ioloop.stop()
        self._server.stop()
        log.info("Stopped API Server...")

    def run(self):
        log.info("Starting API Server...")
        self._server.listen(self._port)
        self._ioloop.start()
