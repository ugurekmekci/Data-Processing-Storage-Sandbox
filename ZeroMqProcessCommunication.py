# -*- coding: utf-8 -*-
import zmq


class IProcessCommunication(object):

    def __init__(self):
        print 1

    def initializeServer(self, bind_port, process_name, **kwargs):
        raise NotImplementedError

    def initializeCli(self, server_ip, port, cli_instance_name):
        raise NotImplementedError


class ZeroMQProvider(IProcessCommunication):

    def __init__(self):
        self.context = zmq.Context()
        self.socket = None

    def initializeServer(self, protocol, bind_port, **kwargs):
        # self.socket = self.context.socket(zmq.REP)
        self.socket = self.context.socket(zmq.PUB)
        socket_connection_str = self._generateServerUrl(protocol, bind_port, **kwargs)
        self.socket.bind(socket_connection_str)
        # self.socket.recv()
        return self.socket

    def _generateServerUrl(self, protocol, bind_port, **kwargs):
        if 'url' in kwargs:
            server_url = kwargs["url"]
        else:
            server_url = "127.0.0.1"
        return protocol + "://" + server_url + ":" + str(bind_port)

    def initializeCli(self, protocol, bind_port, **kwargs):
        self.socket = self.context.socket(zmq.SUB)
        # self.socket = self.context.socket(zmq.REQ)
        socket_connection_str = self._generaterClientUrl(protocol, bind_port, **kwargs)
        self.socket.connect(socket_connection_str)
        self.socket.setsockopt(zmq.SUBSCRIBE, "")
        # self.socket.send("I've got the message...")
        return self.socket

    def _generaterClientUrl(self, protocol, bind_port, **kwargs):
        if 'url' in kwargs:
            server_url = kwargs["url"]
        else:
            server_url = "127.0.0.1"
        return protocol + "://" + server_url + ":" + str(bind_port)




