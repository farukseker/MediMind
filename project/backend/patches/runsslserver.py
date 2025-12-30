# patches/runsslserver.py
import ssl
from django.core.servers.basehttp import ThreadedWSGIServer
import sslserver.management.commands.runsslserver as runsslserver


class PatchedSecureHTTPServer(ThreadedWSGIServer):
    def __init__(self, address, handler_cls, certificate, key, ipv6=False):
        super().__init__(address, handler_cls, ipv6=ipv6)

        context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        context.load_cert_chain(certificate, key)

        self.socket = context.wrap_socket(
            self.socket,
            server_side=True,
        )


runsslserver.SecureHTTPServer = PatchedSecureHTTPServer
