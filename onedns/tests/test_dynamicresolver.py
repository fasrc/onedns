import pytest
import dnslib

from onedns.tests import utils
from onedns.tests import conftest


@pytest.mark.parametrize("qname,qtype,output", conftest.TEST_LOOKUP_DATA)
def test_lookup(dns, qname, qtype, output):
    dns.clear()
    dns.add_host(conftest.HOST, conftest.HOST_IP)
    try:
        a = utils.dnsquery(qname, qtype)
        assert a.short() == output
    finally:
        dns.close()


def test_nxdomain(dns):
    dns.clear()
    try:
        a = utils.dnsquery('unknownhost', dnslib.QTYPE.A)
        assert dnslib.RCODE.get(a.header.rcode) == 'NXDOMAIN'
    finally:
        dns.close()


@pytest.mark.parametrize("name,ip", conftest.TEST_GET_FQDN_DATA)
def test_get_fqdn(dns, name, ip):
    dns.clear()
    dns.add_host(name, ip)
    assert dns.zone[0][0].label[0] == name.split('.')[0]
    assert '.'.join(dns.zone[0][0].label[1:]) == conftest.DOMAIN


def test_daemon(dns):
    dns.close()
    dns.daemon(dns_address=conftest.INTERFACE, dns_port=conftest.PORT,
               tcp=True, testing=True)
