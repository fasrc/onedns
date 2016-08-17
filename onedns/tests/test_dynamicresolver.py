import pytest

import dnslib

from IPy import IP

from onedns import zone
from onedns.tests import utils
from onedns.tests import conftest


def _clear_and_add_test_host(dns, name, ip):
    dns.clear()
    dns.add_host(name, ip)


@pytest.mark.parametrize("qname,qtype,output", conftest.TEST_LOOKUP_DATA)
def test_lookup(dns, qname, qtype, output):
    _clear_and_add_test_host(dns, conftest.HOST, conftest.HOST_IP)
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


def test_daemon(dns):
    dns.close()
    dns.daemon(dns_address=conftest.INTERFACE, dns_port=conftest.PORT,
               tcp=True, testing=True)


@pytest.mark.parametrize("qname,qtype,output", conftest.TEST_LOOKUP_DATA)
def test_remove_host(dns, qname, qtype, output):
    _clear_and_add_test_host(dns, conftest.HOST, conftest.HOST_IP)
    try:
        a = utils.dnsquery(qname, qtype)
        assert a.short() == output
        dns.remove_host(conftest.HOST, conftest.HOST_IP)
        a = utils.dnsquery(qname, qtype)
        assert dnslib.RCODE.get(a.header.rcode) == 'NXDOMAIN'
    finally:
        dns.close()


def test_load_zone(dns):
    new_ip = IP(IP(conftest.HOST_IP).int() + 1)
    new_zone = zone.Zone(conftest.DOMAIN)
    new_zone.add_host(conftest.HOST, new_ip)
    _clear_and_add_test_host(dns, conftest.HOST, conftest.HOST_IP)
    try:
        a = utils.dnsquery(conftest.HOST, dnslib.QTYPE.A)
        assert a.short() == conftest.HOST_IP
        dns.load(new_zone)
        a = utils.dnsquery(conftest.HOST, dnslib.QTYPE.A)
        assert a.short() == str(new_ip)
    finally:
        dns.close()
