import dnslib

from IPy import IP

from onedns import utils
from onedns.tests import conftest


def dnsquery(qname, qtype, server=None, port=None, tcp=False):
    server = server or conftest.INTERFACE
    port = port or conftest.PORT
    q = dnslib.DNSRecord(q=dnslib.DNSQuestion(qname, qtype))
    a_pkt = q.send(server, port, tcp=tcp)
    return dnslib.DNSRecord.parse(a_pkt)


def verify_vm_dns(dns_entries, domain=None):
    domain = domain or conftest.DOMAIN
    for name, ip in dns_entries.items():
        fqdn = utils.get_fqdn(name, domain)
        reverse = IP(ip).reverseName()
        assert dnsquery(fqdn, dnslib.QTYPE.A).short() == ip
        assert dnsquery(reverse, dnslib.QTYPE.PTR).short() == fqdn


def verify_vm_dns_absent(dns_entries, domain=None):
    domain = domain or conftest.DOMAIN
    for name, ip in dns_entries.items():
        fqdn = utils.get_fqdn(name, domain)
        reverse = IP(ip).reverseName()
        q = dnsquery(fqdn, dnslib.QTYPE.A)
        assert dnslib.RCODE.get(q.header.rcode) == 'NXDOMAIN'
        q = dnsquery(reverse, dnslib.QTYPE.PTR)
        assert dnslib.RCODE.get(q.header.rcode) == 'NXDOMAIN'
