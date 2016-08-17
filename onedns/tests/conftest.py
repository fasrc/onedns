import pytest
import dnslib
from IPy import IP

from onedns import zone
from onedns import server
from onedns import resolver
from onedns.tests import vcr
from onedns.clients import one


DOMAIN = 'onedns.test'
INTERFACE = '127.0.0.1'
PORT = 9053
HOST_SHORT = 'testhost'
HOST = '.'.join([HOST_SHORT, DOMAIN])
HOST_IP = '10.242.118.112'
TEST_LOOKUP_DATA = [
    (HOST, dnslib.QTYPE.A, HOST_IP),
    (IP(HOST_IP).reverseName(), dnslib.QTYPE.PTR, HOST + '.')
]
TEST_GET_FQDN_DATA = [
    ('hostwithnodot', '192.168.1.23'),
    ('hostwithdot.', '192.168.1.19'),
]
TEST_GET_FORWARD_DATA = [
    HOST_SHORT,
    HOST_SHORT + '.',
    HOST,
    HOST + '.',
]

@pytest.fixture(scope="function")
def dns(request):
    dns = resolver.DynamicResolver(domain=DOMAIN)
    dns.start(dns_address=INTERFACE, dns_port=PORT, tcp=True)
    request.addfinalizer(dns.close)
    return dns


@pytest.fixture(scope="function")
def oneclient(request):
    """
    NOTE: All fixtures must be function scope to work with VCRPY cassettes
    """
    return one.OneClient()


@pytest.fixture(scope="function")
@vcr.use_cassette()
def vms(oneclient):
    return oneclient.vms()


@pytest.fixture(scope="function")
def onezone():
    z = zone.Zone(DOMAIN)
    z.add_host(HOST_SHORT, HOST_IP)
    for name, ip in TEST_GET_FQDN_DATA:
        z.add_host(name, ip)
    return z
