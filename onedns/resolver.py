from __future__ import print_function
import time
import threading

import dnslib
from dnslib import server

from wrapt import synchronized

from onedns import zone
from onedns import utils
from onedns import exception
from onedns.logger import log


class DynamicResolver(server.BaseResolver):
    """
    Dynamic In-Memory DNS Resolver
    """

    _lock = threading.RLock()

    def __init__(self, domain):
        """
        Initialise resolver from zone list
        Stores RRs as a list of (label, type, rr) tuples
        """
        self.domain = domain
        self.zone = zone.Zone(domain)
        self._tcp_server = None
        self._udp_server = None

    @synchronized(_lock)
    def resolve(self, request, handler):
        """
        Respond to DNS request - parameters are request packet & handler.
        Method is expected to return DNS response
        """
        reply = request.reply()
        qname = request.q.qname
        qtype = request.q.qtype
        try:
            if qtype in (dnslib.QTYPE.A, dnslib.QTYPE.AAAA):
                forward = self.zone.get_forward(qname)
                reply.add_answer(forward)
            elif qtype == dnslib.QTYPE.PTR:
                reverse = self.zone.get_reverse(
                    utils.reverse_to_ip(qname.idna()))
                reply.add_answer(reverse)
                forward = self.zone.get_forward(str(reverse.rdata))
                if forward:
                    reply.add_ar(forward)
        except exception.RecordDoesNotExist:
            reply.header.rcode = dnslib.RCODE.NXDOMAIN
        return reply

    @synchronized(_lock)
    def clear(self):
        self.zone.clear()

    @synchronized(_lock)
    def load(self, zone):
        self.zone = zone

    @synchronized(_lock)
    def add_host(self, name, ip, zone=None):
        z = zone or self.zone
        z.add_host(name, ip)

    @synchronized(_lock)
    def remove_host(self, name, ip, zone=None):
        z = zone or self.zone
        z.remove_host(name, ip)

    def start(self, dns_address='0.0.0.0', dns_port=53,
              api_address='127.0.0.1', api_port=8000, tcp=False, udplen=0,
              log_components="request,reply,truncated,error",
              log_prefix=False):
        logger = server.DNSLogger(log_components, log_prefix)

        log.info("Starting OneDNS (%s:%d) [%s]" %
                 (dns_address or "*", dns_port, "UDP/TCP" if tcp else "UDP"))

        server.DNSHandler.udplen = udplen

        self._udp_server = server.DNSServer(self, port=dns_port,
                                            address=dns_address, logger=logger)
        self._udp_server.start_thread()

        if tcp:
            self._tcp_server = server.DNSServer(self, port=dns_port,
                                                address=dns_address, tcp=True,
                                                logger=logger)
            self._tcp_server.start_thread()

    def close(self):
        for srv in [self._tcp_server, self._udp_server]:
            if srv:
                srv.stop()
                srv.server.socket.close()

    def daemon(self, *args, **kwargs):
        testing = kwargs.pop('testing', False)
        if self._udp_server is None or not self._udp_server.isAlive():
            self.start(*args, **kwargs)
        while self._udp_server.isAlive():
            time.sleep(1)
            if testing:
                break
