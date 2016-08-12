import dnslib

from onedns.tests import conftest


def dnsquery(qname, qtype, server=None, port=None, tcp=False):
    server = server or conftest.INTERFACE
    port = port or conftest.PORT
    q = dnslib.DNSRecord(q=dnslib.DNSQuestion(qname, qtype))
    a_pkt = q.send(server, port, tcp=tcp)
    return dnslib.DNSRecord.parse(a_pkt)
