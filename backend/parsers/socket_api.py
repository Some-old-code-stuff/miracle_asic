# -*- coding: utf-8 -*-
import socket
import json

import re


class SocketApi:
    def __init__(self, host, port=4028):
        self.host = host
        self.port = port

    def command(self, command, arg=None):
        """ Initialize a socket connection,
                send a command (a json encoded dict) and
                receive the response (and decode it).
                """
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)

        try:
            sock.connect((self.host, self.port))
            payload = {'command': command}
            if arg is not None:
                # Parameter must be converted to basestring (no int)
                payload.update({'parameter': str(arg)})

            sock.send(json.dumps(payload).encode())
            received = self._receive(sock)
        finally:
            sock.shutdown(socket.SHUT_RDWR)
            sock.close()
        str_json = received[:-1]
        print(str_json)
        if str_json.startswith(',"SUMMARY":['):
            str_json = str_json.replace(',"SUMMARY":[', '')
            str_json = re.sub(
                r'({"STATUS":\[.+?\])',
                r'\1,"DEVS":',
                str_json
            )
            str_json = str_json.replace('}],"id"', '},"id"')
        print(str_json)
        return json.loads(str_json)

    def _receive(self, sock, size=4096):
        msg = ''
        while 1:
            chunk = sock.recv(size)
            if chunk:
                msg += chunk.decode()
            else:
                break
        return msg

    def __getattr__(self, attr):
        def out(arg=None):
            return self.command(attr, arg)

        return out
