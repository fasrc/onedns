import dnslib

from onedns.tests import conftest


def dnsquery(qname, qtype):
    q = dnslib.DNSRecord(q=dnslib.DNSQuestion(qname, qtype))
    a_pkt = q.send(conftest.INTERFACE, conftest.PORT, tcp=False)
    return dnslib.DNSRecord.parse(a_pkt)
