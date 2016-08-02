import pytest
import dnslib

from IPy import IP

from onedns.tests import conftest


HOST = '.'.join(['testhost', conftest.DOMAIN])
HOST_IP = '10.242.118.112'
TEST_LOOKUP_DATA = [
    (HOST, dnslib.QTYPE.A, HOST_IP),
    (IP(HOST_IP).reverseName(), dnslib.QTYPE.PTR, HOST + '.')
]
TEST_GET_FQDN_DATA = [
    ('hostwithnodot', '192.168.1.23'),
    ('hostwithdot.', '192.168.1.19'),
]


@pytest.mark.parametrize("qname,qtype,output", TEST_LOOKUP_DATA)
def test_lookup(dns, qname, qtype, output):
    dns.clear()
    dns.add_host(HOST, HOST_IP)
    try:
        q = dnslib.DNSRecord(q=dnslib.DNSQuestion(qname, qtype))
        a_pkt = q.send(conftest.INTERFACE, conftest.PORT, tcp=False)
        a = dnslib.DNSRecord.parse(a_pkt)
        assert a.short() == output
    finally:
        dns.close()


def test_nxdomain(dns):
    dns.clear()
    try:
        q = dnslib.DNSRecord(q=dnslib.DNSQuestion(
            'unknownhost', dnslib.QTYPE.A))
        a_pkt = q.send(conftest.INTERFACE, conftest.PORT, tcp=False)
        a = dnslib.DNSRecord.parse(a_pkt)
        assert dnslib.RCODE.get(a.header.rcode) == 'NXDOMAIN'
    finally:
        dns.close()


@pytest.mark.parametrize("name,ip", TEST_GET_FQDN_DATA)
def test_get_fqdn(dns, name, ip):
    dns.clear()
    dns.add_host(name, ip)
    assert dns.zone[0][0].label[0] == name.split('.')[0]
    assert '.'.join(dns.zone[0][0].label[1:]) == conftest.DOMAIN


def test_daemon(dns):
    dns.close()
    dns.daemon(dns_address=conftest.INTERFACE, dns_port=conftest.PORT,
               tcp=True, testing=True)
