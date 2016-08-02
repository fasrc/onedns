# -*- coding: utf-8 -*-
from __future__ import print_function
import time

import dnslib
from dnslib import server
from dnslib import dns

from IPy import IP


class DynamicResolver(server.BaseResolver):
    """
    Dynamic In-Memory DNS Resolver
    """

    def __init__(self, domain, one_kwargs={}):
        """
        Initialise resolver from zone list
        Stores RRs as a list of (label, type, rr) tuples
        """
        self.domain = domain
        self.zone = []
        self._tcp_server = None
        self._udp_server = None

    def resolve(self, request, handler):
        """
        Respond to DNS request - parameters are request packet & handler.
        Method is expected to return DNS response
        """
        reply = request.reply()
        qname = request.q.qname
        qtype = dnslib.QTYPE[request.q.qtype]
        for name, rtype, rr in self.zone:
            # Check if label & type match
            if qname == name and (qtype in [rtype, 'ANY'] or rtype == 'CNAME'):
                reply.add_answer(rr)
                # Check for A/AAAA records associated with reply and
                # add in additional section
                if rtype in ['CNAME', 'NS', 'MX', 'PTR']:
                    for a_name, a_rtype, a_rr in self.zone:
                        if a_name == rr.rdata.label and a_rtype in ['A', 'AAAA']:
                            reply.add_ar(a_rr)
        if not reply.rr:
            reply.header.rcode = dnslib.RCODE.NXDOMAIN
        return reply

    def clear(self):
        self.zone = []

    def add_host(self, name, ip):
        self._add_forward(name, ip)
        self._add_reverse(ip, name)

    def _get_fqdn(self, name):
        if not name.endswith(self.domain):
            if name.endswith('.'):
                return name + self.domain
            else:
                return '.'.join([name, self.domain])
        return name

    def _add_forward(self, name, ip):
        f = dnslib.RR(rname=dnslib.DNSLabel(self._get_fqdn(name)),
                      rtype=dnslib.QTYPE.reverse['A'],
                      rclass=dnslib.CLASS.reverse['IN'],
                      rdata=dns.A(ip))
        self.zone.append((f.rname, 'A', f))

    def _add_reverse(self, ip, name):
        ip = IP(ip)
        r = dnslib.RR(rname=dnslib.DNSLabel(ip.reverseName()),
                      rtype=dnslib.QTYPE.reverse['PTR'],
                      rclass=dnslib.CLASS.reverse['IN'],
                      rdata=dns.PTR(self._get_fqdn(name)))
        self.zone.append((r.rname, 'PTR', r))

    def start(self, dns_address='0.0.0.0', dns_port=53,
              api_address='127.0.0.1', api_port=8000, tcp=False, udplen=0,
              log="request,reply,truncated,error", log_prefix=False):
        logger = server.DNSLogger(log, log_prefix)

        print("Starting OneDNS (%s:%d) [%s]" %
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
